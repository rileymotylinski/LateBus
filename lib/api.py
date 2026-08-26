from requests import get
from collections import defaultdict
from datetime import datetime
from google.transit import gtfs_realtime_pb2
import numpy
import csv
import os

"""
    purpose: handles ALL parsing/calling of data from api
    - rate limiting
        - using rate limit library
    - easily adding endpoints
        - these will be hardcoded into the class

    - handling response codes
        - try catch blocks...on what?
    - data validation
        - custom solution
"""

class MetroApi():

    def __init__(self):
        self._base_url = "https://svc.metrotransit.org/nextrip"

    def _get_handler(self,url):
        res = get(url)
        try:
            return res.json()
        except:
            print(res.status_code)
    def gtfs_feed(self):

        feed = gtfs_realtime_pb2.FeedMessage()
        response = self._get_handler('https://svc.metrotransit.org/mtgtfs/tripupdates.pb')

        feed.ParseFromString(response.content)
        return feed

    def directions(self, route_id):
        return self._get_handler(self._base_url + f"/directions/{route_id}")
    def stops(self,route_id):
        res = {}
        for direction in self.directions(route_id):
            print(direction)
            res[direction["direction_id"]] = self.stops_dir(route_id, direction)
        return res
    def stops_dir(self,route_id, direction_id):
        return self._get_handler(self._base_url + f"/stops/{route_id}/{direction_id}")
def remove_past(s: str, c: chr):
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
STOP_LOCATIONS: dict[int, numpy.array[int,int]] = {}
STOP_DESCRIPTIONS: dict[str,str] = {} # matches "description" -> stop id
SHAPE_IDS: dict[tuple[int,str], int] = {} # (route_id, trip_id) -> shape_id
SHAPES: defaultdict[int, list[numpy.array[int,int,int]]] = defaultdict(list) # shape_id -> [(lat1,lon1, dist_traveled), ...]
ROUTE_IDS: int = []
HASHED_ROUTE_IDS = {}
TRIP_IDS = defaultdict(set) # matches trip id -> route_id
SCHEDULE = defaultdict(dict) # matches (trip_id, stop_id) -> expected arrival time

def parse_time(time: str):
    """
    time - HH:MM:SS format
    """
    parts = time.split(":")

    if len(parts) != 3:
        print("improper time format")
        return
    return (int(parts[0]),int(parts[1]),int(parts[2]))

  
try:
    dir = os.path.dirname(__file__)
    stops = os.path.join(dir,"Schedule", "stops.txt")
    trips = os.path.join(dir, "Schedule", "trips.txt")
    routes = os.path.join(dir,"Schedule", "routes.txt")
    shapes = os.path.join(dir,"Schedule", "shapes.txt")
    stop_times = os.path.join(dir,"Schedule", "stop_times.txt")

    with open(stops, "r") as csvfile:
        next(csvfile)
        reader = csv.reader(csvfile)
        
        for row in reader:
            stop_id = row[0]
            stop_description = row[2]
            
            stop_lat = row[4]
            stop_lon = row[5]

            STOP_IDS.append(stop_id)   
            STOP_LOCATIONS[stop_id] = (numpy.array((stop_lat,stop_lon)))
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
            trip_id = r[0]
            hour, min, second = parse_time(r[2])
            stop_id = r[3]
            route_id = TRIP_IDS.get(trip_id, None)
            
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

except FileNotFoundError:
    print("File does not exist")








        
