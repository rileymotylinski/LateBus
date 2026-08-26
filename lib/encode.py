from lib.api import SHAPE_IDS, HASHED_ROUTE_IDS, ROUTE_IDS, STOP_LOCATIONS, SHAPES, ROUTE_STOP_SEQUENCES
from datetime import datetime
from lib.api import MetroApi

TOTAL_ROUTES = len(ROUTE_IDS)
ROUTE_STOP_SEQUENCES = {}
api = MetroApi()

class Bus:
    def __init__(self,route_id, trip_id, destination_stop_id, expected: int,actual: int,timestamp: int, lat: float, lon: float, direction_id: int):
        self.route_id = route_id
        self.trip_id = trip_id
        self.destination_stop_id = destination_stop_id
        self.expected = datetime.fromtimestamp(expected)
        self.actual = datetime.fromtimestamp(actual)
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

    vec += one_hot_encode(d.route_id) # encoding route_id
    vec += [1] if d.expected.weekday >= 5 else [0] # weekday/weekend
    vec += [1] if (d.expected.hour >= 6 and d.expected.hour <= 9) or (d.expected.hour >= 15 and (d.expected.hour <= 18 and d.expected.minute <= 30)) else [0] # rush hour (per metro transit)

    vec += [ROUTE_STOP_SEQUENCES[d.route_id][d.direction_id][d.destination_stop_id]]
    
    dest_point = STOP_LOCATIONS[d.destination_stop_id]
    shape_points = SHAPES[SHAPE_IDS[(d.route_id, d.trip_id)]]
    min_dist = shape_points[0]
    for point in shape_points:
        pass




