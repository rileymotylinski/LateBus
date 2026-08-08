from requests import get
import pprint
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
        return [s["place_code"] for s in get(self._base_url + f"/stops/{route_id}/{direction_id}").json()]

    def get_route_ids(self):
        return [r["route_id"] for r in self.routes()]

    def departures(self,stop_id):
        res =  get(self._base_url + f"/{stop_id}").json()
        try:
            return res["departures"]
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
  
try:
    dir = os.path.dirname(__file__)
    routes = os.path.join(dir,"Schedule", "stops.txt")
   
    with open(routes, "r") as csvfile:
        next(csvfile)
        reader = csv.reader(csvfile)
        
        for row in reader:
            STOP_IDS.append(row[0])
            

except FileNotFoundError:
    print("File does not exist")
    get_bus_schedule()







        
