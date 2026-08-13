from requests import get
from collections import defaultdict
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

def get_bus_schedule():
    # TODO
    # pulls static bus schedule from metro
    # fall back is calling api directly
    # some sort of check to make sure all routes are on schedule? I don't know if this is always true.
    pass

STOP_IDS = []
STOP_DESCRIPTIONS = {}
TRIP_IDS = defaultdict(set)
  
try:
    dir = os.path.dirname(__file__)
    routes = os.path.join(dir,"Schedule", "stops.txt")
    trips = os.path.join(dir, "Schedule", "trips.txt")
   
    with open(routes, "r") as csvfile:
        next(csvfile)
        reader = csv.reader(csvfile)
        
        for row in reader:
            STOP_IDS.append(row[0])   
            STOP_DESCRIPTIONS[row[2]] = row[0]    
        csvfile.close()

    with open(trips, "r") as csvfile:
        next(csvfile)
        reader = csv.reader(csvfile)

        for row in reader:
            route_id = row[0]
            trip_id = row[2]
            TRIP_IDS[route_id].add(trip_id)
        csvfile.close()

except FileNotFoundError:
    print("File does not exist")
    get_bus_schedule()







        
