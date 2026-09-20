from lib.scripts.metro_constants import HASHED_ROUTE_IDS, ROUTE_IDS, STOP_LOCATIONS, ROUTE_STOP_SEQUENCES
from lib.classes.PositionSnapshot import PositionSnapshot
from lib.classes.api import MetroApi
import geopy.distance
from lib.scripts.far_status import AVG_DIST_BETWEEN_STOPS
from math import sqrt

TOTAL_ROUTES = len(ROUTE_IDS)
ROUTE_STOP_SEQUENCES = {}
api = MetroApi()

def one_hot_encode(route_id):
    vec = [0] * TOTAL_ROUTES
    vec[HASHED_ROUTE_IDS[route_id]] = 1
    return vec

def encode(d: PositionSnapshot):
    vec = []

    # idea: add direction id to encoded vector? directly?
    vec += one_hot_encode(d.route_id) # encoding route_id

    # as-the-crow-flies distance
    dest = STOP_LOCATIONS[d.destination_stop_id]
    snaphot_loc = (d.lat, d.lon)
    dist = sqrt(geopy.distance.geodesic(dest, snaphot_loc).km)

    vec += [1] if (d.expected.weekday() >= 5) else [0] # weekday/weekend
    vec += [1] if (d.expected.hour >= 6 and d.expected.hour <= 9) or (d.expected.hour >= 15 and (d.expected.hour <= 18 and d.expected.minute <= 30)) else [0] # rush hour (per metro transit)

    vec += [ROUTE_STOP_SEQUENCES[d.route_id][d.direction_id][d.destination_stop_id]] # stop sequence i.e. the 5th stop is 5

    
    vec += [dist]
    vec += [int(dist < AVG_DIST_BETWEEN_STOPS // 2)]




