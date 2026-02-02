--- Question 1
CREATE OR REPLACE EXTERNAL TABLE `zoomcamp.yellow_tripdata_jan_jun_ext`
OPTIONS (
  format = 'PARQUET',
  uris = [
    'gs://terraform-demo-485708-terra-bucket/yellow_tripdata_2024-01.parquet',
    'gs://terraform-demo-485708-terra-bucket/yellow_tripdata_2024-02.parquet',
    'gs://terraform-demo-485708-terra-bucket/yellow_tripdata_2024-03.parquet',
    'gs://terraform-demo-485708-terra-bucket/yellow_tripdata_2024-04.parquet',
    'gs://terraform-demo-485708-terra-bucket/yellow_tripdata_2024-05.parquet',
    'gs://terraform-demo-485708-terra-bucket/yellow_tripdata_2024-06.parquet'
  ]
);


CREATE TABLE `zoomcamp.yellow_tripdata_jan_jun` AS
SELECT * 
FROM `zoomcamp.yellow_tripdata_jan_jun_ext`;

--- Question 1
select count(*) from zoomcamp.yellow_tripdata_jan_jun;

--- Question 2
-- Count distinct PULocationID in External Table
SELECT COUNT(DISTINCT PULocationID) AS distinct_pickups
FROM `zoomcamp.yellow_tripdata_jan_jun_ext`;

-- Count distinct PULocationID in Regular Table
SELECT COUNT(DISTINCT PULocationID) AS distinct_pickups
FROM `zoomcamp.yellow_tripdata_jan_jun`;

-- Question 3
SELECT PULocationID FROM `zoomcamp.yellow_tripdata_jan_jun`;

SELECT PULocationID, DOLocationID FROM `zoomcamp.yellow_tripdata_jan_jun`;

--Question 4

SELECT COUNT(fare_amount) FROM `zoomcamp.yellow_tripdata_jan_jun`
WHERE fare_amount = 0;

--- QUESTION 5
CREATE TABLE `terraform-demo-485708.zoomcamp.yellow_tripdata_optimized`
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID AS
SELECT *
FROM `terraform-demo-485708.zoomcamp.yellow_tripdata_jan_jun`;

-- QUESTION 6
SELECT DISTINCT(VendorID) FROM `terraform-demo-485708.zoomcamp.yellow_tripdata_jan_jun`
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' and '2024-03-15';
 
 SELECT DISTINCT(VendorID) FROM `terraform-demo-485708.zoomcamp.yellow_tripdata_optimized`
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' and '2024-03-15';
 
