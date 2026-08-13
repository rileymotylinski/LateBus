from lib.api import MetroApi, STOP_DESCRIPTIONS

class BusRoute:
    api: MetroApi = MetroApi()
    def __init__(self, route_id):
        self.route_id = str(route_id)
        self.stops = []
        # all the sotps along an entire route
        for d in self.api.directions(self.route_id):
            self.stops += self.api.stops(self.route_id,d["direction_id"])

    def route_departures(self):
        for stop in self.stops:
       
            stop_id = STOP_DESCRIPTIONS.get(stop["description"], None)
            if stop_id:
                for departure in self.api.departures(stop_id):
                    if departure["route_id"] == self.route_id:
                        pass
                        # print(departure)
            else:
                print(f"unable to find {stop["description"]}")
                