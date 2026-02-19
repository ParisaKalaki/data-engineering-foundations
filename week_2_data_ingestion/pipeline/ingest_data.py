#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm
import click
import requests

dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]

@click.command()
@click.option('--pg-user', default='root', help='PostgreSQL username')
@click.option('--pg-pass', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default='5432', help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--trip-url', default='https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet', help='URL of the Parquet trip data')
@click.option('--zones-url', default='https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv', help='URL of the taxi zones CSV')
@click.option('--chunksize', default=100000, type=int, help='Chunk size for ingestion')
@click.option('--trip-table', default='green_taxi_data', help='Target table name for trip data')
@click.option('--zones-table', default='taxi_zones', help='Target table name for zones')
def run(pg_user, pg_pass, pg_host, pg_port, pg_db, trip_url, zones_url, chunksize, trip_table, zones_table):

    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')

    # --- Download and ingest Parquet trip data ---
    local_trip_file = 'temp_trip.parquet'
    print(f"Downloading trip data from {trip_url} ...")
    r = requests.get(trip_url, stream=True)
    r.raise_for_status()
    with open(local_trip_file, 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
    print("Trip data download complete.")

    df_trip = pd.read_parquet(local_trip_file, engine='pyarrow')
    total_rows = len(df_trip)
    print(f"Total trip rows: {total_rows}")

    first = True
    for start in tqdm(range(0, total_rows, chunksize)):
        end = min(start + chunksize, total_rows)
        df_chunk = df_trip.iloc[start:end]
        if first:
            df_chunk.head(0).to_sql(name=trip_table, con=engine, if_exists='replace')
            first = False
        df_chunk.to_sql(name=trip_table, con=engine, if_exists='append')
    print(f"Trip data ingested into table '{trip_table}'.")

    # --- Download and ingest zones CSV ---
    local_zones_file = 'taxi_zone_lookup.csv'
    print(f"Downloading zones data from {zones_url} ...")
    r = requests.get(zones_url)
    r.raise_for_status()
    with open(local_zones_file, 'wb') as f:
        f.write(r.content)
    print("Zones download complete.")

    df_zones = pd.read_csv(local_zones_file)
    df_zones.to_sql(name=zones_table, con=engine, if_exists='replace', index=False)
    print(f"Zones data ingested into table '{zones_table}'.")


if __name__ == '__main__':
    run()
