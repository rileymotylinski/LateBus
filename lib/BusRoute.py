from lib.api import MetroApi

class BusRoute:
    api: MetroApi = MetroApi()
    def __init__(self, route_id):
        self.route_id = str(route_id)
        self.stops = [self.api.stops(self.route_id,d["direction_id"]) for d in self.api.directions(self.route_id)]

    def route_departures(self):
        for direction in self.api.directions(self.route_id):
            # need a way to match direction -> stop_id
