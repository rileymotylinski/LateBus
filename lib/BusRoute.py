from lib.api import MetroApi

class BusRoute:
    api: MetroApi = MetroApi()
    def __init__(self, route_id):
        self.route_id = str(route_id)

    def stops(self):
        stops = []
        for d in self.api.directions(self.route_id):
            stops += self.api.stops(self.route_id,d["direction_id"])
        return stops

