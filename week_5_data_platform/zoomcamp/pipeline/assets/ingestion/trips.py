"""@bruin
name: ingestion.trips
description: Ingest NYC Taxi trip data from public API
type: python
image: python:3.11
connection: duckdb-default
materialization:
  type: table
  strategy: append
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
  - name: pickup_location_id
    type: int
    description: Location ID where trip started
  - name: dropoff_location_id
    type: int
    description: Location ID where trip ended
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
  - name: payment_type
    type: int
    description: Payment method code
@bruin"""

from datetime import datetime

def materialize() -> list[dict]:
    """
    Ingest NYC Taxi trip data from public API.
    For this demo, returns sample data.
    In production, this would fetch from live API.
    """
    trips = [
        {
            "trip_id": 1,
            "taxi_type": "yellow",
            "pickup_datetime": "2025-02-18 08:15:00",
            "dropoff_datetime": "2025-02-18 08:35:00",
            "pickup_location_id": 42,
            "dropoff_location_id": 151,
            "distance_miles": 2.3,
            "fare_amount": 15.50,
            "tip_amount": 3.00,
            "total_amount": 20.30,
            "payment_type": 1
        },
        {
            "trip_id": 2,
            "taxi_type": "green",
            "pickup_datetime": "2025-02-18 09:20:00",
            "dropoff_datetime": "2025-02-18 09:45:00",
            "pickup_location_id": 74,
            "dropoff_location_id": 213,
            "distance_miles": 4.1,
            "fare_amount": 22.75,
            "tip_amount": 5.00,
            "total_amount": 29.75,
            "payment_type": 1
        },
        {
            "trip_id": 3,
            "taxi_type": "yellow",
            "pickup_datetime": "2025-02-18 10:05:00",
            "dropoff_datetime": "2025-02-18 10:25:00",
            "pickup_location_id": 151,
            "dropoff_location_id": 42,
            "distance_miles": 2.1,
            "fare_amount": 14.00,
            "tip_amount": 2.50,
            "total_amount": 18.50,
            "payment_type": 2
        }
    ]
    
    print(f"Ingested {len(trips)} NYC Taxi trips")
    return trips




