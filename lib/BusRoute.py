from lib.api import MetroApi, STOP_DESCRIPTIONS, SCHEDULE
from datetime import datetime

class BusRoute:
    api: MetroApi = MetroApi()
    def __init__(self, route_id):
        self.route_id = str(route_id)
        self.stops = {}
        # all the stops along an entire route
        for d in self.api.directions(self.route_id):
            for stop in self.api.stops(self.route_id,d["direction_id"]):
                
                self.stops[stop["place_code"]] = stop["description"]
          

    def route_departures(self):
        schedule = {}
        for stop in self.stops.values(): # pulls descriptions
            
            stop_id = STOP_DESCRIPTIONS.get(stop, None)
      
            if stop_id:
                res = self.api.departures(stop_id)
             
                for departure in res:
                    ident = (departure["trip_id"], stop_id)
                    expected_arrival = SCHEDULE.get(ident, None)
                    if expected_arrival and departure["route_id"] == self.route_id:
                        arrival_times = (expected_arrival, datetime.fromtimestamp(departure["departure_time"]))
                        schedule[ident] = arrival_times
        return schedule

                