import logging
import os
from typing import Callable, Optional

from pyspark.conf import SparkConf
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.protobuf.functions import from_protobuf

from .enums import *
from .schema_helper import apply_avro_schema_from_registry
from .spark_sink_config import SparkSinkConfig


class SparkSinkConnector:
    """
    A connector for reading data from Kafka and writing to S3 in Delta or Hudi format.
    """

    def __init__(self, connector_mode: ConnectorMode, config: Optional[SparkSinkConfig] = None,
                 logger: Optional[logging.Logger] = None,
                 logging_level: str = 'INFO'):
        """
        Initialize the SparkSinkConnector with configuration.

        Args:
            connector_mode: Whether to use streaming mode or batch mode
            config: Configuration object for the connector
            logger: Optional logger instance
        """
        self.foreach_batch_fn = None
        self.config = config or SparkSinkConfig()
        self._setup_logger(logger)
        self.connector_mode = connector_mode
        self.dataframe = None
        self.writer = None
        self.spark_session = self._create_spark_session()
        self.spark_session.sparkContext.setLogLevel(logging_level)

    def _setup_logger(self, logger: Optional[logging.Logger] = None):
        """Set up the logger for this class."""
        if logger:
            self.logger = logger
        else:
            self.logger = logging.getLogger(__name__)
            logging.basicConfig(
                format=self.config.logger_format,
                level=logging.INFO
            )

    def _create_spark_session(self) -> SparkSession:
        """
        Create and configure a Spark session.

        Returns:
            SparkSession: Configured Spark session

        Raises:
            Exception: If Spark session creation fails
        """
        try:
            spark_conf = SparkConf()
            spark_conf.set("spark.appName", f"s3_sink_{os.path.basename(__file__)}")

            # S3 configuration
            spark_conf.set("spark.hadoop.fs.s3a.access.key", self.config.s3_access_key)
            spark_conf.set("spark.hadoop.fs.s3a.secret.key", self.config.s3_secret_key)
            spark_conf.set("spark.hadoop.fs.s3a.endpoint", self.config.s3_endpoint)
            spark_conf.set("spark.hadoop.fs.s3a.path.style.access", "true")
            spark_conf.set("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
            spark_conf.set("spark.hadoop.fs.s3a.connection.ssl.enabled", "false")

            # Spark SQL and Delta configuration
            spark_conf.set("spark.sql.session.timeZone", "Asia/Tehran")
            spark_conf.set("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
            spark_conf.set("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
            spark_conf.set("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
            spark_conf.set("spark.sql.legacy.timeParserPolicy", "LEGACY")

            # Packages
            spark_conf.set("spark.jars.packages", self.config.spark_jars)

            # Extra configurations
            if self.config.spark_extra_configs is not None:
                for key, value in self.config.spark_extra_configs.items():
                    spark_conf.set(key, value)

            spark = SparkSession.builder.config(conf=spark_conf).getOrCreate()
            self.logger.info("✅ Spark session created successfully.")
            return spark
        except Exception as e:
            self.logger.error(f"❌ Failed to create Spark session: {e}")
            raise

    def read_from_kafka(self, **kwargs) -> 'SparkSinkConnector':
        """
        Read data from Kafka topic.

        Returns:
            self: For method chaining
        """
        self.config.update_configs(**kwargs)
        kafka_options = {
            "kafka.bootstrap.servers": self.config.kafka_broker,
            "subscribe": self.config.kafka_topic,
            "minOffsetsPerTrigger": self.config.min_offset,
            "maxOffsetsPerTrigger": self.config.max_offset,
            "failOnDataLoss": self.config.fail_on_data_loss,
            "startingOffsets": self.config.starting_offsets,
            "kafkaConsumer.pollTimeoutMs": self.config.kafka_session_timeout,
            "kafka.request.timeout.ms": self.config.kafka_request_timeout,
            "kafka.session.timeout.ms": self.config.kafka_session_timeout,
        }
        self.logger.info(f"Kafka configurations are: ")
        self.logger.info(kafka_options)

        # Add authentication options if credentials are provided
        if self.config.kafka_user and self.config.kafka_password:
            kafka_options.update({
                "kafka.sasl.mechanism": "SCRAM-SHA-512",
                "kafka.security.protocol": "SASL_PLAINTEXT",
                "kafka.sasl.jaas.config": (
                    f"org.apache.kafka.common.security.scram.ScramLoginModule required "
                    f"username='{self.config.kafka_user}' password='{self.config.kafka_password}';"
                )
            })

        # Extra options
        if self.config.kafka_extra_options is not None:
            kafka_options.update(self.config.kafka_extra_options)

        # Build the reader with all options
        reader = self.spark_session.readStream if self.connector_mode == ConnectorMode.STREAM else self.spark_session.read
        reader = reader.format("kafka")
        for key, value in kafka_options.items():
            reader = reader.option(key, value)

        self.dataframe = reader.load()
        self.logger.info(f"✅ Successfully read Kafka batch.")
        return self

    def get_dataframe(self) -> DataFrame:
        """
        Returns the Spark DataFrame.

        Returns:
            self.dataframe
        """
        return self.dataframe

    def get_logger(self) -> logging.Logger:
        """
        Returns the logger.

        Returns:
            self.logger
        """
        return self.logger

    def set_dataframe(self, dataframe: DataFrame):
        """
        Sets the Spark DataFrame.

        Args:
            dataframe: Spark DataFrame
        """
        self.dataframe = dataframe

    def apply_schema_from_file(self, kind: SchemaKind, file_name: str, message_name: str) -> 'SparkSinkConnector':
        """
        Apply schema from a file to the DataFrame.

        Args:
            kind: Type of schema (AVRO or PROTOBUF)
            file_name: Path to the schema file
            message_name: Name of the message in the schema

        Returns:
            self: For method chaining
        """
        if not self.dataframe:
            self.logger.error("❌ DataFrame not initialized. Call read_from_kafka() first.")
            raise ValueError("DataFrame not initialized")

        if kind == SchemaKind.PROTOBUF:
            self.dataframe = self.dataframe.select(
                from_protobuf("value", message_name, file_name).alias("event")
            )
            self.dataframe = self.dataframe.select("event.*")
            self.logger.info(f"✅ Applied Protobuf schema from file: {file_name}")
        else:
            self.logger.warning(f"⚠️ Schema kind {kind} not implemented for file-based schemas")

        return self

    def apply_schema_from_registry(self, kind: SchemaKind = SchemaKind.AVRO) -> 'SparkSinkConnector':
        """
        Apply schema from registry to the DataFrame.

        Args:
            kind: Type of schema (AVRO or PROTOBUF)

        Returns:
            self: For method chaining
        """
        if not self.dataframe:
            self.logger.error("❌ DataFrame not initialized. Call read_from_kafka() first.")
            raise ValueError("DataFrame not initialized")

        if kind == SchemaKind.AVRO:
            self.dataframe = apply_avro_schema_from_registry(self.dataframe, self.config.schema_registry_url, self.logger)
        else:
            self.logger.warning(f"⚠️ Schema kind {kind} not implemented for registry-based schemas")

        return self

    def foreach_batch(self,
                      foreach_batch_fn: Optional[Callable[[DataFrame, int], None]] = None) -> 'SparkSinkConnector':
        """
        Gets a foreach batch function.

        Args:
            foreach_batch_fn: Function that takes a DataFrame and int
        """
        self.foreach_batch_fn = foreach_batch_fn
        return self

    def transform(self, transformation_fn: Optional[Callable[[DataFrame], DataFrame]] = None) -> 'SparkSinkConnector':
        """
        Apply transformations to the DataFrame.

        Args:
            transformation_fn: Function that takes a DataFrame and returns a transformed DataFrame

        Returns:
            self: For method chaining
        """
        if not self.dataframe:
            self.logger.error("❌ DataFrame not initialized. Call read_from_kafka() first.")
            raise ValueError("DataFrame not initialized")

        if transformation_fn:
            self.dataframe = transformation_fn(self.dataframe)
            self.logger.info("✅ Custom transformations applied to DataFrame")

        return self

    def write_to_s3(self,
                    open_table_format: OpenTableFormat = None,
                    output_mode: ConnectorOutputMode = None,
                    **kwargs) -> 'SparkSinkConnector':
        """
        Configure writing data to S3 in Hudi format.

        Args:
            open_table_format: Hudi or Delta
            output_mode: Output mode (append, upsert or overwrite)

        Returns:
            self: For method chaining
        """
        self.config.update_configs(**kwargs)

        if not self.dataframe:
            self.logger.error("❌ DataFrame not initialized. Call read_from_kafka() first.")
            raise ValueError("DataFrame not initialized")

        if self.connector_mode == ConnectorMode.STREAM:
            self.writer = self.dataframe.writeStream
        else:
            self.writer = self.dataframe.write

        if open_table_format is not None:
            self.writer = self.writer.format(open_table_format.value)
        if self.config.partition_key is not None:
            self.writer = self.writer.partitionBy(self.config.partition_key)
        if self.config.hoodie_options is not None:
            self.writer = self.writer.options(**self.config.hoodie_options)
        if self.config.checkpoint_path is not None:
            self.writer = self.writer.option("checkpointLocation", self.config.checkpoint_path)
        if self.config.table_path is not None:
            self.writer = self.writer.option("path", self.config.table_path)

        if self.foreach_batch_fn is not None:
            self.writer = self.writer.foreachBatch(self.foreach_batch_fn)

        if self.connector_mode == ConnectorMode.BATCH and output_mode is not None:
            self.writer = self.writer.mode(output_mode)

        if self.connector_mode == ConnectorMode.STREAM:
            self.writer = self.writer.trigger(**self.config.trigger_mode)

        self.logger.info(f"✅ Configured to write to {self.config.table_path}.")

        return self

    def start(self) -> None:
        """
        Start the writing job and await termination.
        """
        if not self.writer:
            self.logger.error("❌ Writer not initialized. Call write_to_s3() first.")
            raise ValueError("Writer not initialized")

        if self.connector_mode == ConnectorMode.STREAM:
            self.writer.start().awaitTermination()
        else:
            self.writer.save()
