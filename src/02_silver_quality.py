# Databricks notebook source
from pyspark.sql import functions as F
from pyspark.sql.window import Window

dbutils.widgets.text("catalog", "adb_lakehouse_circuit_dev")
catalog = dbutils.widgets.get("catalog")

customers = spark.table(f"{catalog}.bronze.customers")
orders = spark.table(f"{catalog}.bronze.orders")

# Tolerant casts are essential in the validation layer: malformed source values
# become NULL and are then captured by the quality rules instead of failing the job.
customers_typed = customers.withColumn("signup_date_parsed", F.expr("try_cast(signup_date AS date)"))
customer_checks = [
    (F.col("customer_id").isNull() | (F.trim("customer_id") == ""), "MISSING_CUSTOMER_ID"),
    (F.col("full_name").isNull() | (F.trim("full_name") == ""), "MISSING_FULL_NAME"),
    (~F.col("email").rlike(r"^[^@\s]+@[^@\s]+\.[^@\s]+$"), "INVALID_EMAIL"),
    (~F.col("country_code").rlike(r"^[A-Z]{2}$"), "INVALID_COUNTRY_CODE"),
    (F.col("signup_date_parsed").isNull(), "INVALID_SIGNUP_DATE"),
]
customer_error_array = F.array(*[F.when(condition, F.lit(code)) for condition, code in customer_checks])
customers_checked = customers_typed.withColumn("_quality_errors", F.filter(customer_error_array, lambda x: x.isNotNull()))

customer_window = Window.partitionBy("customer_id").orderBy(F.col("_ingested_at").desc())
valid_customers = (
    customers_checked.filter(F.size("_quality_errors") == 0)
    .withColumn("_row_number", F.row_number().over(customer_window))
    .filter(F.col("_row_number") == 1)
    .drop("_row_number", "signup_date")
    .withColumnRenamed("signup_date_parsed", "signup_date")
)
invalid_customers = customers_checked.filter(F.size("_quality_errors") > 0)

valid_customers.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"{catalog}.silver.customers")
invalid_customers.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"{catalog}.quarantine.customers")

valid_customer_ids = valid_customers.select("customer_id").distinct().withColumn("_known_customer", F.lit(True))
orders_typed = (
    orders.withColumn("order_timestamp_parsed", F.expr("try_cast(order_timestamp AS timestamp)"))
    .withColumn("quantity_parsed", F.expr("try_cast(quantity AS int)"))
    .withColumn("unit_price_parsed", F.expr("try_cast(unit_price AS decimal(18,2))"))
    .join(valid_customer_ids, "customer_id", "left")
)
order_checks = [
    (F.col("order_id").isNull() | (F.trim("order_id") == ""), "MISSING_ORDER_ID"),
    (F.col("_known_customer").isNull(), "UNKNOWN_CUSTOMER"),
    (F.col("order_timestamp_parsed").isNull(), "INVALID_ORDER_TIMESTAMP"),
    (F.col("quantity_parsed").isNull() | (F.col("quantity_parsed") <= 0), "INVALID_QUANTITY"),
    (F.col("unit_price_parsed").isNull() | (F.col("unit_price_parsed") <= 0), "INVALID_UNIT_PRICE"),
    (~F.col("status").isin("PROCESSING", "SHIPPED", "COMPLETED", "CANCELLED"), "INVALID_STATUS"),
]
order_error_array = F.array(*[F.when(condition, F.lit(code)) for condition, code in order_checks])
orders_checked = orders_typed.withColumn("_quality_errors", F.filter(order_error_array, lambda x: x.isNotNull()))

order_window = Window.partitionBy("order_id").orderBy(F.col("_ingested_at").desc())
valid_orders = (
    orders_checked.filter(F.size("_quality_errors") == 0)
    .withColumn("_row_number", F.row_number().over(order_window))
    .filter(F.col("_row_number") == 1)
    .drop("_row_number", "_known_customer", "order_timestamp", "quantity", "unit_price")
    .withColumnRenamed("order_timestamp_parsed", "order_timestamp")
    .withColumnRenamed("quantity_parsed", "quantity")
    .withColumnRenamed("unit_price_parsed", "unit_price")
    .withColumn("order_amount", F.round(F.col("quantity") * F.col("unit_price"), 2))
)
invalid_orders = orders_checked.filter(F.size("_quality_errors") > 0).drop("_known_customer")

valid_orders.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"{catalog}.silver.orders")
invalid_orders.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"{catalog}.quarantine.orders")

