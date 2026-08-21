from requests import get
from collections import defaultdict
from datetime import datetime
from google.transit import gtfs_realtime_pb2
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

    def routes(self):

        return get(self._base_url + "/routes").json()

    def _raw_direction_call(self,route_id):

        # initial call to verify a bus in running/has stops/etc.
        return get(self._base_url + f"/directions/{route_id}")
    
    def is_running(self,route_id):

        return self._raw_direction_call(route_id).ok
    
    def directions(self, route_id):

        return self._raw_direction_call(route_id).json()

    def stops(self,route_id, direction_id):

        """
        metro api does not return __ALL__ stops; i'm not sure why, it is very undocumented
        """
        res = get(self._base_url + f"/stops/{route_id}/{direction_id}")
        if res.ok:
            return res.json()
        else:
            print(res)

    def get_route_ids(self):

        return [r["route_id"] for r in self.routes()]

    def departures(self,stop_id):
 
        res =  get(self._base_url + f"/{stop_id}").json()
        try:
            return res["departures"]
        except:
            print(f"{res["detail"]}: no departures found")
            return []

    def route_departures(self,route_id, direction_id, place_code):
   
        res =  get(self._base_url + f"/{route_id}/{direction_id}/{place_code}").json()
        try:
            return res
        except:
            print(f"{res["detail"]}: no departures found")
            return []

    def gtfs_feed(self):
        feed = gtfs_realtime_pb2.FeedMessage()
        response = get('https://svc.metrotransit.org/mtgtfs/tripupdates.pb')
        feed.ParseFromString(response.content)
        return feed


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

def get_bus_schedule():
    # TODO
    # pulls static bus schedule from metro
    # fall back is calling api directly
    # some sort of check to make sure all routes are on schedule? I don't know if this is always true.
    pass

STOP_IDS = [] # list of all stop ids 
STOP_DESCRIPTIONS = {} # matches "description" -> stop id
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
    routes = os.path.join(dir,"Schedule", "stops.txt")
    trips = os.path.join(dir, "Schedule", "trips.txt")
    stop_times = os.path.join(dir,"Schedule", "stop_times.txt")

    with open(routes, "r") as csvfile:
        next(csvfile)
        reader = csv.reader(csvfile)
        
        for row in reader:
            stop_id = row[0]
            stop_description = row[2]
            STOP_IDS.append(row[0])   
            # some stops include mutliple gates; i'm considering them as a single stop
            #  because arrival times will be neglibile between them. this is an obvious trade off, 
            # but the api does not return the gate number from the stop detail so it needs to be done
            STOP_DESCRIPTIONS[clean_stop_name(stop_description)] =  stop_id    
        csvfile.close()

    with open(trips, "r") as csvfile:
        next(csvfile)
        reader = csv.reader(csvfile)

        for row in reader:
            route_id = row[0]
            trip_id = row[2]
            TRIP_IDS[trip_id] = route_id
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

            SCHEDULE[route_id][(trip_id, stop_id)] = expected
    print(f"found {total_invalid} invalid times")

except FileNotFoundError:
    print("File does not exist")
    get_bus_schedule()







        
