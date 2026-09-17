from collections import defaultdict
import numpy
import os
import csv
from datetime import datetime
from numpy.typing import NDArray
from lib.classes.api import MetroApi

def remove_past(s: str, c: str):
    try: 
        char_location = s.index(c)
        if  char_location > 0 and char_location < len(s):
            s = s[:char_location]
    except:
        pass
    return s

def clean_stop_name(stop_name: str):
    try:
        if stop_name.lower().index("gate") > 0:
            stop_name = remove_past(remove_past(stop_name, "-"), "&")
    except:
        pass
    return stop_name.strip()


STOP_IDS: list[str] = [] # list of all stop ids 
STOP_LOCATIONS: dict[int, NDArray] = {}
STOP_DESCRIPTIONS: dict[str,str] = {} # matches "description" -> stop id
SHAPE_IDS: dict[tuple[str,str], str] = {} # (route_id, trip_id) -> shape_id
SHAPES: defaultdict[str, list[NDArray]] = defaultdict(list) # shape_id -> [(lat1,lon1, dist_traveled), ...]
ROUTE_IDS: list[str] = []
HASHED_ROUTE_IDS = {} # route_id -> linear index
TRIP_IDS: dict[str, str] = {} # matches trip_id -> route_id
TRIPS: dict[str, list[str]] = defaultdict(list) # matches route_id -> trip_ids
SCHEDULE = defaultdict(dict) # matches route_id -> (trip_id, stop_id) -> expected arrival time
ROUTE_STOP_SEQUENCES = {} # route_id -> {direction_id1 -> {stop_id -> stop_sequence}}

def parse_time(time: str) -> tuple[int,int,int]:
    """
    time - HH:MM:SS format
    """
    parts = time.split(":")

    if len(parts) != 3:
        print("improper time format")
        return (0,0,0)
    return (int(parts[0]),int(parts[1]),int(parts[2]))

  
try:
    dir = os.path.join(os.path.dirname(__file__), "..", "Schedule")
    stops = os.path.join(dir, "stops.txt")
    trips = os.path.join(dir, "trips.txt")
    routes = os.path.join(dir, "routes.txt")
    shapes = os.path.join(dir, "shapes.txt")
    stop_times = os.path.join(dir, "stop_times.txt")

    with open(stops, "r") as csvfile:
        next(csvfile)
        reader = csv.reader(csvfile)
        
        for row in reader:
            stop_id = row[0]
            stop_description = row[2]
            
            stop_lat = row[4]
            stop_lon = row[5]

            STOP_IDS.append(stop_id)   
            STOP_LOCATIONS[int(stop_id)] = (numpy.array((stop_lat,stop_lon)))
            # some stops include mutliple gates; i'm considering them as a single stop
            #  because arrival times will be neglibile between them. this is an obvious trade off, 
            # but the api does not return the gate number from the stop detail so it needs to be done
            STOP_DESCRIPTIONS[clean_stop_name(stop_description)] =  stop_id    
        csvfile.close()

    with open(trips, "r") as csvfile:
        
        reader = csv.reader(csvfile)
        next(reader)

        for row in reader:
            route_id = row[0]
            trip_id = row[2]
            shape_id = row[7]

            TRIP_IDS[trip_id] = route_id
            TRIPS[route_id].append(trip_id)
            SHAPE_IDS[(route_id, trip_id)] = shape_id
        csvfile.close()

    with open(shapes,"r") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)

        for row in reader:
            shape_id = row[0]
            lat = row[1]
            lon = row[2]
            dist_traveled = row[4]

            SHAPES[shape_id].append(numpy.array((lat,lon,dist_traveled)))
        csvfile.close()

    total_invalid = 0
    with open (stop_times, "r",  newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        
        for r in reader:
            trip_id = str(r[0])
            hour, min, second = parse_time(r[2])
            if (hour,min,second) == (0,0,0):
                print("failed to parse time")
                continue
            
            stop_id = str(r[3])
            route_id = str(TRIP_IDS.get(trip_id, None))
            
            if (hour > 23):
                total_invalid += 1
                continue

            if not route_id:
                print(f"uanble to find route for trip_id: {trip_id}")
            
            expected = datetime.today().replace(hour=hour,minute=min, second=second)

            SCHEDULE[route_id][(trip_id, stop_id)] = expected.timestamp()
    with open(routes, "r") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            ROUTE_IDS.append(row[0])
    ROUTE_IDS.sort()
    for i in range(len(ROUTE_IDS)):
        HASHED_ROUTE_IDS[ROUTE_IDS[i]] = i
    print(f"found {total_invalid} invalid times")

    api = MetroApi()
    all_stops = {}
    for route_id in ROUTE_IDS:
        temp: dict[int, list[dict[str, str]]] = api.stops(route_id)
        
        for direction in temp:
       
            direction_stops_sequence: dict[str, int] = {}
            
            for i in range(len(temp[direction])):
                direction_stops_sequence[temp[direction][i]["place_code"]] = i # basically telling you what order the bus stops come in
            all_stops[direction] = direction_stops_sequence
        ROUTE_STOP_SEQUENCES[route_id] = stops
except FileNotFoundError as e:
    print(f"{e} File does not exist")