"""@bruin
name: staging.trips
description: Clean and transform raw NYC Taxi trip data
type: duckdb.sql
depends_on:
  - ingestion.trips
  - ingestion.payment_lookup
materialization:
  type: table
  strategy: create+replace
columns:
  - name: trip_id
    type: int
    primary_key: true
    description: Unique trip identifier
  - name: taxi_type
    type: string
    description: Type of taxi (yellow, green)
  - name: pickup_datetime
    type: timestamp
    description: Trip pickup timestamp
  - name: dropoff_datetime
    type: timestamp
    description: Trip dropoff timestamp
  - name: distance_miles
    type: float
    description: Trip distance in miles
  - name: fare_amount
    type: float
    description: Metered fare in USD
  - name: tip_amount
    type: float
    description: Tip amount in USD
  - name: total_amount
    type: float
    description: Total amount charged in USD
  - name: duration_minutes
    type: float
    description: Trip duration in minutes
  - name: payment_method
    type: string
    description: Payment method description
quality_checks:
  - name: trip_id_not_null
    column: trip_id
    condition: not_null
  - name: total_amount_positive
    column: total_amount
    condition: positive
  - name: distance_positive
    column: distance_miles
    condition: positive
@bruin"""

SELECT
  t.trip_id,
  t.taxi_type,
  CAST(t.pickup_datetime AS TIMESTAMP) as pickup_datetime,
  CAST(t.dropoff_datetime AS TIMESTAMP) as dropoff_datetime,
  t.pickup_location_id,
  t.dropoff_location_id,
  CAST(t.distance_miles AS FLOAT) as distance_miles,
  CAST(t.fare_amount AS FLOAT) as fare_amount,
  CAST(t.tip_amount AS FLOAT) as tip_amount,
  CAST(t.total_amount AS FLOAT) as total_amount,
  ROUND(EXTRACT(EPOCH FROM (CAST(t.dropoff_datetime AS TIMESTAMP) - CAST(t.pickup_datetime AS TIMESTAMP))) / 60, 2) as duration_minutes,
  COALESCE(p.payment_method, 'Unknown') as payment_method
FROM ingestion.trips t
LEFT JOIN ingestion.payment_lookup p ON t.payment_type = p.payment_type
WHERE CAST(t.pickup_datetime AS TIMESTAMP) >= '{{ start_datetime }}'
  AND CAST(t.pickup_datetime AS TIMESTAMP) < '{{ end_datetime }}'
