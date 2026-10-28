# Databricks notebook source
from pyspark.sql import functions as F, types as T

dbutils.widgets.text("catalog", "adb_lakehouse_circuit_dev")
dbutils.widgets.dropdown("reset_checkpoint", "false", ["false", "true"])
catalog = dbutils.widgets.get("catalog")
reset_checkpoint = dbutils.widgets.get("reset_checkpoint") == "true"

landing_root = "abfss://landing@stlakecircuitdev01.dfs.core.windows.net"
checkpoint_root = "abfss://checkpoints@stlakecircuitdev01.dfs.core.windows.net/bronze"

customer_schema = T.StructType([
    T.StructField("customer_id", T.StringType()),
    T.StructField("full_name", T.StringType()),
    T.StructField("email", T.StringType()),
    T.StructField("country_code", T.StringType()),
    T.StructField("signup_date", T.StringType()),
])
order_schema = T.StructType([
    T.StructField("order_id", T.StringType()),
    T.StructField("customer_id", T.StringType()),
    T.StructField("order_timestamp", T.StringType()),
    T.StructField("quantity", T.StringType()),
    T.StructField("unit_price", T.StringType()),
    T.StructField("status", T.StringType()),
])


def ingest(entity, schema):
    checkpoint = f"{checkpoint_root}/{entity}"
    if reset_checkpoint:
        dbutils.fs.rm(checkpoint, True)
    source = f"{landing_root}/{entity}"
    target = f"{catalog}.bronze.{entity}"
    query = (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "csv")
        .option("header", "true")
        .schema(schema)
        .load(source)
        # Unity Catalog does not support input_file_name(). Auto Loader exposes
        # governed file metadata through the hidden _metadata struct instead.
        .withColumn("_source_file", F.col("_metadata.file_path"))
        .withColumn("_ingested_at", F.current_timestamp())
        .writeStream.option("checkpointLocation", checkpoint)
        .trigger(availableNow=True)
        .toTable(target)
    )
    query.awaitTermination()


ingest("customers", customer_schema)
ingest("orders", order_schema)

