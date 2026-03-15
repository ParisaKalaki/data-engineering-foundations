
import dataclasses
import json
from dataclasses import dataclass

@dataclass
class Ride:
    PULocationID: int
    DOLocationID: int
    passenger_count: int
    trip_distance: float
    total_amount: float
    lpep_pickup_datetime: int  # epoch milliseconds
    lpep_dropoff_datetime: int  # epoch milliseconds


def ride_from_row(row):
    return Ride(
        PULocationID=int(row['PULocationID']),
        DOLocationID=int(row['DOLocationID']),
        lpep_pickup_datetime=int(row['lpep_pickup_datetime'].timestamp() * 1000),
        lpep_dropoff_datetime=int(row['lpep_dropoff_datetime'].timestamp() * 1000),
        passenger_count=int(row['passenger_count']),
        trip_distance=float(row['trip_distance']),
        total_amount=float(row['total_amount']),
    )


def ride_serializer(ride):
    return json.dumps(dataclasses.asdict(ride)).encode('utf-8')

def ride_deserializer(data):
    ride_dict = json.loads(data)
    return Ride(**ride_dict)