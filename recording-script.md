# Recording script

## 0:00 — Hook

**On screen:** Final Databricks Workflow graph, then Gold table results.

**Say:** “In this tutorial we’ll build a production-style Azure Databricks ETL pipeline with managed identity, Unity Catalog, Auto Loader, quarantine rules and a scheduled workflow—without storing a single cloud access key.”

## 0:25 — Architecture

**On screen:** README architecture diagram.

Explain Landing → Bronze → Silver/Quarantine → Gold, and identify the operational role of checkpoints.

## 1:30 — Azure resources

**On screen:** Resource group overview, with subscription ID and account email obscured.

Show the Databricks workspace, ADLS Gen2 account and Access Connector. Show the Storage Blob Data Contributor assignment.

## 3:30 — Unity Catalog connection

**On screen:** Storage credential and two external locations.

Explain that managed identity removes embedded keys. Do not expose tokens, object IDs or subscription IDs.

## 5:00 — Synthetic data

**On screen:** Customer and order CSV files.

Point out duplicates and deliberately invalid values that will demonstrate quarantine behavior.

## 6:30 — Bronze ingestion

**On screen:** `01_bronze_ingestion.py` and the first Workflow task.

Explain Auto Loader, explicit schemas, source metadata, `availableNow`, and durable checkpoints. Run the notebook.

## 9:00 — Silver and quarantine

**On screen:** `02_silver_quality.py`, then query valid and invalid tables.

Explain typed columns, referential integrity, error arrays and deterministic deduplication.

## 13:00 — Gold layer

**On screen:** `03_gold_aggregates.py`, `gold.customer_360`, and `gold.daily_sales`.

Explain business-ready outputs and why cancelled orders are excluded from revenue.

## 15:30 — Production Workflow

**On screen:** `databricks.yml`, Workflow DAG, run timeline.

Explain dependency ordering, concurrency control, schedule pause status, bundle validation and deployment.

## 18:00 — Results and close

**On screen:** Row-count verification query and Gold results.

Recap reliability, governance, observability and cost controls. Invite viewers to clone the repository and suggest the next pipeline topic.

