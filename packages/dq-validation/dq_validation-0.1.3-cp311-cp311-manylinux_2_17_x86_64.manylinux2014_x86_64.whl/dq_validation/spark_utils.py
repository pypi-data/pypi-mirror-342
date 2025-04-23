import tempfile
from typing import Optional, Tuple, Any
from contextlib import contextmanager
import multiprocessing
import math
import os
import psutil
from .logger import logger

import pyarrow.parquet as pq
from pyspark.sql import SparkSession


_DEFAULT_HEAP_SIZE_EXTRA_ROOM_PER_CORE = 268435456


def _get_cgroup_memory() -> int:
    max_memory_str = None
    if os.path.isfile("/sys/fs/cgroup/memory.max"):
        with open("/sys/fs/cgroup/memory.max", "r") as f:
            max_memory_str = f.read().strip()
    elif os.path.isfile("/sys/fs/cgroup/memory/memory.limit_in_bytes"):
        with open("/sys/fs/cgroup/memory/memory.limit_in_bytes", "r") as f:
            max_memory_str = f.read().strip()

    max_memory = None
    if max_memory_str == "max":
        # Fallback to available virtual memory size
        max_memory = psutil.virtual_memory().available
    elif max_memory_str is not None:
        try:
            max_memory = int(max_memory_str)
        except ValueError:
            pass

    if max_memory is not None:
        return max_memory
    else:
        logger.info("Unable to determine available memory from cgroup, assuming 4G")
        return 4 * 1024 * 1024 * 1024


def _get_uncompressed_parquet_size(path: str):
    def is_parquet(filename: str):
        return filename.endswith(".parquet")
    def get_uncompressed_size(file_path: str):
        parquet_file = pq.ParquetFile(file_path)
        metadata = parquet_file.metadata
        uncompressed_size = 0
        for i in range(metadata.num_row_groups):
            row_group = metadata.row_group(i)
            for j in range(row_group.num_columns):
                column = row_group.column(j)
                uncompressed_size += column.total_uncompressed_size
        return uncompressed_size
    if os.path.isfile(path) and is_parquet(path):
        uncompressed_size = get_uncompressed_size(path)
        return uncompressed_size
    # Path might be a subdir as obtained by `partitionBy`
    elif os.path.isdir(path):
        total_uncompressed_size = 0
        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            total_uncompressed_size += _get_uncompressed_parquet_size(file_path)
        return total_uncompressed_size
    else:
        return 0


def _get_num_partitions(
        paths: Optional[list[str]],
        available_memory: int,
        cpu_count: int,
) -> int:
    """Determine the number of partitions s.t. each partition is as big as possible
    while still making sure all cores are occupied."""
    def get_file_or_dir_size(path):
        if path.endswith(".parquet"):
            return _get_uncompressed_parquet_size(path)
        else:
            if os.path.isfile(path):
                size = os.path.getsize(path)
            elif os.path.isdir(path):
                total_size = 0
                for dirpath, dirnames, filenames in os.walk(path):
                    for f in filenames:
                        fp = os.path.join(dirpath, f)
                        total_size += os.path.getsize(fp)
                size = total_size
            else:
                raise ValueError(f"The path {path} is neither a file nor a directory.")
        return size

    # Default number of partitions in spark
    default_num_partitions = 200
    if paths is None or len(paths) == 0:
        return default_num_partitions
    file_size = max([get_file_or_dir_size(path) for path in paths])
    if file_size == 0:
        return default_num_partitions

    # Don't make the partitions smaller than 36MiB
    megabyte_in_bytes = 1024 * 1024
    min_partition_size = 32 * megabyte_in_bytes

    # Try to make partitions as big as possible s.t. each CPU is saturated,
    # while accounting for 50% overhead in spark.
    task_per_cpu = 3  # try to get at least this many tasks/partitions per CPU
    max_target_partition_size = max(
        int(0.5 * available_memory / (task_per_cpu * cpu_count)) // megabyte_in_bytes * megabyte_in_bytes,
        min_partition_size
    )

    target_partition_size = max_target_partition_size
    while (
        # If the file is small enough that it cannot be split across all cores,
        # divide the partition size further.
        int(file_size / target_partition_size) < (task_per_cpu * cpu_count)
    ):
        # Don't go smaller than the minimum parition size
        if target_partition_size / 2 < min_partition_size:
            break
        target_partition_size = target_partition_size / 2

    logger.info(f"File size: {file_size}")
    logger.info(f"Max target partition size: {max_target_partition_size}")
    logger.info(f"Target partition size: {target_partition_size}")

    num_partitions = int(math.ceil(file_size / target_partition_size))

    return num_partitions


def _determine_optimal_spark_settings(
        files: Optional[list[str]] = None,
        heap_size: Optional[int] = None,
        heap_size_extra_room: Optional[int] = None,
        heap_size_extra_room_per_core: Optional[int] = None
) -> list[Tuple[str, str]]:
    cpu_count = multiprocessing.cpu_count()

    if heap_size is not None:
        spark_memory = heap_size
    else:
        cgroup_memory = _get_cgroup_memory()
        two_gb_in_bytes = 2147483648
        if heap_size_extra_room is not None:
            pass
        elif heap_size_extra_room_per_core is not None:
            heap_size_extra_room = heap_size_extra_room_per_core * cpu_count
        else:
            heap_size_extra_room = _DEFAULT_HEAP_SIZE_EXTRA_ROOM_PER_CORE * cpu_count
        spark_memory = max(cgroup_memory - heap_size_extra_room, two_gb_in_bytes)

    spark_memory_4096 = (spark_memory // 4096) * 4096
    num_partitions = _get_num_partitions(files, spark_memory, cpu_count)

    settings = [
        ("spark.sql.shuffle.partitions", str(num_partitions)),
        ("spark.default.parallelism", str(num_partitions)),
        ("spark.driver.cores", str(cpu_count)),
        ("spark.driver.memory", str(spark_memory_4096)),
    ]

    return settings


def _create_spark_session(
        name: str = "local_spark_session",
        parallelism: int = 8,
        config: list[Tuple[str, Any]] = [],
        java_temp_dir: str = "/scratch",
        java_user_home_dir: str = "/scratch",
) -> SparkSession:
    """
    :param name: The name of the spark session.
    :param parallelism: The size of the executor pool computing internal spark tasks.
    :param config: Additional config settings to set on the spark config.
    :param java_temp_dir: Location for the JVM to store temp files.
    :param java_user_home_dir: Location for the user home directory as seen by the JVM.
    :return: The spark session.
    """
    os.environ["SPARK_EXECUTOR_POOL_SIZE"] = str(parallelism)
    os.environ["JDK_JAVA_OPTIONS"] = f'-Duser.home="{java_user_home_dir}" -Djava.io.tmpdir="{java_temp_dir}"'

    ss = (
        SparkSession.builder
        .appName(name)
        .master("local[*]")
    )
    for (key, value) in config:
        ss = ss.config(key, value)

    logger.info("Spark settings:\n" + f"\n".join([str(x) for x in config]))

    return ss.getOrCreate()


@contextmanager
def spark_session(
        temp_dir: str = "/scratch",
        name: str = "Spark",
        input_files: list[str] = None,
        heap_size: Optional[int] = None,
        heap_size_extra_room: Optional[int] = None,
        heap_size_extra_room_per_core: Optional[int] = None,
        config: list[Tuple[str, str]] = [],
):
    """
    Create a spark session and configure it according to the enclave environment.

    **Parameters**:
    - `temp_dir`: Where to store temporary data such as persisted data frames
      or shuffle data.
    - `name`: An optional name for this spark session.
    - `input_files`: A list of input files on the basis of which the partition
      size is determined.
    - `heap_size`: The heap size to use for Spark. If not set, sensible defaults are chosen.
    - `heap_size_extra_room`: How much extra room to leave for non-JVM tasks. If not set, sensible defaults are chosen.
    - `heap_size_extra_room_per_core`: Same as `heap_size_extra_room` but scaled with the number of cores. This is the default behavior.
    - `config`: Extra settings to pass to the Spark session builder.

    **Example**:

    ```python
    import decentriq_util as dq

    # Path to a potentially very large file
    input_csv_path = "/input/my_file.csv"

    # Automatically create and configure a spark session and
    # make sure it's being stopped at the end.
    with dq.spark.spark_session(input_files=[input_csv_path]) as ss:
        # Read from a CSV file
        df = ss.read.csv(input_csv_path, header=False).cache()

        # Perform any pyspark transformations
        print(f"Original number of rows: {df.count()}")
        result_df = df.limit(100)

        # Write the result to an output file
        result_df.write.parquet("/output/my_file.parquet")
    ```
    """
    with tempfile.TemporaryDirectory(dir=temp_dir, prefix="java-") as java_tmp:
        with tempfile.TemporaryDirectory(dir=temp_dir, prefix="spark-") as spark_tmp:
            config_dict = dict(config)
            optimal_settings = _determine_optimal_spark_settings(
                input_files,
                heap_size=heap_size,
                heap_size_extra_room=heap_size_extra_room,
                heap_size_extra_room_per_core=heap_size_extra_room_per_core,
            )
            for key, value in optimal_settings:
                if key not in config_dict:
                    config.append((key, value))
            if "spark.local.dir" not in config_dict:
                config.append(
                    ("spark.local.dir", spark_tmp)
                )
            ss = _create_spark_session(name=name, java_temp_dir=java_tmp, java_user_home_dir=java_tmp, config=config)
            try:
                yield ss
            finally:
                try:
                    ss.stop()
                except:
                    pass
