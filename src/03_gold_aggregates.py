# Databricks notebook source
from pyspark.sql import functions as F

dbutils.widgets.text("catalog", "adb_lakehouse_circuit_dev")
catalog = dbutils.widgets.get("catalog")

customers = spark.table(f"{catalog}.silver.customers")
orders = spark.table(f"{catalog}.silver.orders")
revenue_orders = orders.filter(F.col("status") != "CANCELLED")

customer_metrics = revenue_orders.groupBy("customer_id").agg(
    F.countDistinct("order_id").alias("order_count"),
    F.round(F.sum("order_amount"), 2).alias("lifetime_value"),
    F.max("order_timestamp").alias("last_order_at"),
)
customer_360 = (
    customers.join(customer_metrics, "customer_id", "left")
    .fillna({"order_count": 0, "lifetime_value": 0})
    .select("customer_id", "full_name", "email", "country_code", "signup_date", "order_count", "lifetime_value", "last_order_at")
)
customer_360.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"{catalog}.gold.customer_360")

daily_sales = (
    revenue_orders
    .groupBy(F.to_date("order_timestamp").alias("order_date"), "status")
    .agg(F.countDistinct("order_id").alias("order_count"), F.round(F.sum("order_amount"), 2).alias("revenue"))
)
daily_sales.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"{catalog}.gold.daily_sales")

