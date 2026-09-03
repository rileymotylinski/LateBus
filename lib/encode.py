from lib.api import HASHED_ROUTE_IDS, ROUTE_IDS, STOP_LOCATIONS, ROUTE_STOP_SEQUENCES
from datetime import datetime
from lib.api import MetroApi
from math import sqrt

TOTAL_ROUTES = len(ROUTE_IDS)
ROUTE_STOP_SEQUENCES = {}
api = MetroApi()

class Bus:
    def __init__(self,route_id, trip_id, destination_stop_id, expected: int,timestamp: int, lat: float, lon: float, direction_id: int):
        self.route_id = route_id
        self.trip_id = trip_id
        self.destination_stop_id = destination_stop_id
        self.expected = datetime.fromtimestamp(expected)
        self.timestamp = datetime.fromtimestamp(timestamp)
        self.lat = lat
        self.lon = lon
        self.direction_id = direction_id

def one_hot_encode(route_id):
    vec = [0] * TOTAL_ROUTES
    vec[HASHED_ROUTE_IDS[route_id]] = 1
    return vec

def encode(d: Bus):
    vec = []

    # idea: add direction id to encoded vector? directly?
    vec += one_hot_encode(d.route_id) # encoding route_id
    vec += [1] if d.expected.weekday >= 5 else [0] # weekday/weekend
    vec += [1] if (d.expected.hour >= 6 and d.expected.hour <= 9) or (d.expected.hour >= 15 and (d.expected.hour <= 18 and d.expected.minute <= 30)) else [0] # rush hour (per metro transit)

    vec += [ROUTE_STOP_SEQUENCES[d.route_id][d.direction_id][d.destination_stop_id]] # stop sequence i.e. the 5th stop is 5

    # as-the-crow-flies distance
    dest_lon, dest_lat = STOP_LOCATIONS[d.destination_stop_id]
    dist = sqrt((dest_lat - d.lat)**2 + (dest_lon - d.lon))
    vec += [dist]




