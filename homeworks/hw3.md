# Homework 3 – BigQuery & GCS

## Overview
This repository contains my solution for Homework 3, where I worked with **Yellow Taxi Trip Records (January 2024 – June 2024)** using **Google Cloud Storage (GCS)** and **BigQuery**.

The goal of this homework was to:
- Upload Parquet files to a GCS bucket
- Create an **External Table** in BigQuery referencing those files
- Create a **regular (materialized) BigQuery table** from the external table
- Run analytical queries to compare performance and data scanned

---

## Data Upload
The Yellow Taxi Parquet files were **uploaded manually** to a **GCP Bucket** (not via orchestration tools like Kestra or Airflow), as required by the assignment.

---

## BigQuery Setup

### External Table
An **external table** was created in BigQuery that references the Parquet files stored in the GCS bucket.  
The data itself remains in **GCS**, and BigQuery only stores the schema and file references.

### Materialized Table
A **regular (materialized) BigQuery table** was created from the external table.  
This table stores the data directly inside BigQuery and is used for query performance comparison.

---

## Queries
All SQL queries used to answer the homework questions are stored in:
[hw3](path-to-file)

This includes:
- Counting distinct `PULocationID`
- Comparing estimated bytes processed between external and materialized tables
- Column selection queries
- Partitioning and clustering strategy queries

---

## Notes
- The data was **not loaded into BigQuery using orchestration**
- External tables were created using **PARQUET format**
- The homework focuses on understanding **storage vs query engines**, **external vs internal tables**, and **query optimization**

---

## Tools Used
- Google Cloud Storage (GCS)
- BigQuery
- SQL
