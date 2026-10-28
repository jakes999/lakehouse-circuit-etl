-- Run before the second bundle execution: both first queries should return 0.
SELECT COUNT(*) AS incremental_customer_rows_before
FROM adb_lakehouse_circuit_dev.bronze.customers
WHERE _source_file LIKE '%customers_2026-10-28.csv';

SELECT COUNT(*) AS incremental_order_rows_before
FROM adb_lakehouse_circuit_dev.bronze.orders
WHERE _source_file LIKE '%orders_2026-10-28.csv';

-- Run after the second bundle execution: expect 4 customers and 5 orders.
SELECT _source_file, COUNT(*) AS rows_ingested
FROM adb_lakehouse_circuit_dev.bronze.customers
GROUP BY _source_file
ORDER BY _source_file;

SELECT _source_file, COUNT(*) AS rows_ingested
FROM adb_lakehouse_circuit_dev.bronze.orders
GROUP BY _source_file
ORDER BY _source_file;

-- Expected final layer counts: 11, 6, 12 and 7.
SELECT 'silver_customers' AS table_name, COUNT(*) AS row_count
FROM adb_lakehouse_circuit_dev.silver.customers
UNION ALL
SELECT 'quarantine_customers', COUNT(*)
FROM adb_lakehouse_circuit_dev.quarantine.customers
UNION ALL
SELECT 'silver_orders', COUNT(*)
FROM adb_lakehouse_circuit_dev.silver.orders
UNION ALL
SELECT 'quarantine_orders', COUNT(*)
FROM adb_lakehouse_circuit_dev.quarantine.orders;

-- Expected result: 11 customers, 11 revenue orders, 1530.18 revenue.
SELECT
  COUNT(*) AS customers,
  SUM(order_count) AS revenue_orders,
  ROUND(SUM(lifetime_value), 2) AS revenue
FROM adb_lakehouse_circuit_dev.gold.customer_360;

-- Proves that the customer update won during latest-record deduplication.
SELECT customer_id, full_name, email
FROM adb_lakehouse_circuit_dev.silver.customers
WHERE customer_id = 'C003';

-- Shows the two new invalid order outcomes.
SELECT order_id, customer_id, _quality_errors
FROM adb_lakehouse_circuit_dev.quarantine.orders
WHERE order_id IN ('O1019', 'O1020')
ORDER BY order_id;

