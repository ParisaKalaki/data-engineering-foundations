"""@bruin
name: reports.trips_report
description: Daily NYC Taxi trips analytics report
type: duckdb.sql
depends_on:
  - staging.trips
materialization:
  type: table
  strategy: time_interval
  incremental_key: trip_date
  time_granularity: date
columns:
  - name: trip_date
    type: date
    primary_key: true
    description: Trip date
  - name: taxi_type
    type: string
    primary_key: true
    description: Type of taxi (yellow, green)
  - name: total_trips
    type: int
    description: Total number of trips
    checks:
      - name: non_negative
  - name: total_revenue
    type: float
    description: Total fare amount in USD
    checks:
      - name: positive
  - name: total_tips
    type: float
    description: Total tips in USD
  - name: avg_fare
    type: float
    description: Average fare per trip
  - name: avg_distance
    type: float
    description: Average distance per trip
  - name: avg_duration_minutes
    type: float
    description: Average trip duration in minutes
@bruin"""

SELECT
  DATE(pickup_datetime) as trip_date,
  taxi_type,
  COUNT(*) as total_trips,
  SUM(fare_amount) as total_revenue,
  SUM(tip_amount) as total_tips,
  ROUND(AVG(fare_amount), 2) as avg_fare,
  ROUND(AVG(distance_miles), 2) as avg_distance,
  ROUND(AVG(duration_minutes), 2) as avg_duration_minutes
FROM staging.trips
WHERE DATE(pickup_datetime) >= '{{ start_date }}'
  AND DATE(pickup_datetime) < '{{ end_date }}'
GROUP BY DATE(pickup_datetime), taxi_type
ORDER BY trip_date DESC, taxi_type
