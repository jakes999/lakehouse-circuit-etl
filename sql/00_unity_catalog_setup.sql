-- Run as a Unity Catalog metastore administrator or catalog owner.
CREATE CATALOG IF NOT EXISTS adb_lakehouse_circuit_dev;
USE CATALOG adb_lakehouse_circuit_dev;

CREATE SCHEMA IF NOT EXISTS bronze COMMENT 'Raw append-only ingestion tables';
CREATE SCHEMA IF NOT EXISTS silver COMMENT 'Validated and conformed tables';
CREATE SCHEMA IF NOT EXISTS gold COMMENT 'Business-ready aggregates';
CREATE SCHEMA IF NOT EXISTS quarantine COMMENT 'Rejected records with quality errors';
CREATE SCHEMA IF NOT EXISTS operations COMMENT 'Operational audit and pipeline metadata';

-- These objects already exist in the tutorial environment. Keep this script as
-- reproducible infrastructure documentation; uncomment only in a new workspace.
-- CREATE STORAGE CREDENTIAL cred_lakehouse_circuit_dev
-- WITH AZURE_MANAGED_IDENTITY (
--   ACCESS_CONNECTOR_ID = '/subscriptions/<id>/resourceGroups/rg-lakehouse-circuit-dev/providers/Microsoft.Databricks/accessConnectors/ac-lakehouse-circuit-dev'
-- );
-- CREATE EXTERNAL LOCATION ext_lakehouse_landing_dev
-- URL 'abfss://landing@stlakecircuitdev01.dfs.core.windows.net/'
-- WITH (STORAGE CREDENTIAL cred_lakehouse_circuit_dev);
-- CREATE EXTERNAL LOCATION ext_lakehouse_checkpoints_dev
-- URL 'abfss://checkpoints@stlakecircuitdev01.dfs.core.windows.net/'
-- WITH (STORAGE CREDENTIAL cred_lakehouse_circuit_dev);

SHOW SCHEMAS;
SHOW EXTERNAL LOCATIONS;
