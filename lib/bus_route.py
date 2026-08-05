from lib.api import MetroApi

class BusRoute():
    def __init__(self, route_id):
        self.route_id = route_id
        self.stops = {}

        api = MetroApi()

        directions = api.directions(self.route_id)

        for d in directions:
            self.stops[d["direction_name"]] = api.stops(self.route_id, d["direction_id"])

        