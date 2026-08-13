from lib.api import MetroApi

class BusStop():
    api: MetroApi = MetroApi()

    def __init__(self, stop_id):
        self.stop_id = stop_id
        self.departures = self.api.departures(self.stop_id)

    def update_departures(self):
        self.departures = self.api.departures(self.stop_id)

   