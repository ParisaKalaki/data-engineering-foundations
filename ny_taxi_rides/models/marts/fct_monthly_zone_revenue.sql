-- models/marts/fct_monthly_zone_revenue.sql

WITH trips_union AS (

    -- Pickup-side revenue
    SELECT
        TIMESTAMP_TRUNC(pickup_datetime, MONTH) AS month,
        pickup_location_id AS location_id,
        pickup_zone AS zone_name,
        'pickup' AS trip_event,
        service_type,
        total_amount AS revenue,
        trip_id
    FROM {{ ref('fct_trips') }}
    WHERE pickup_datetime IS NOT NULL

    UNION ALL

    -- Dropoff-side revenue
    SELECT
        TIMESTAMP_TRUNC(dropoff_datetime, MONTH) AS month,
        dropoff_location_id AS location_id,
        dropoff_zone AS zone_name,
        'dropoff' AS trip_event,
        service_type,
        total_amount AS revenue,
        trip_id
    FROM {{ ref('fct_trips') }}
    WHERE dropoff_datetime IS NOT NULL
)

SELECT
    month,
    location_id,
    zone_name,
    trip_event,                 -- 👈 explicit!
    service_type,
    SUM(revenue) AS total_revenue,
    COUNT(DISTINCT trip_id) AS total_trips
FROM trips_union
GROUP BY
    month,
    location_id,
    zone_name,
    trip_event,
    service_type
ORDER BY
    month,
    location_id,
    trip_event,
    zone_name
