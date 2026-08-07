from lib.api import MetroApi

class BusStop():
    api: MetroApi = MetroApi()

    def __init__(self, stop_id):
        self.stop_id = stop_id

    def next_departure(self):
        departures = self.api.departures(self.stop_id)
        if len(departures) != 0:
            return departures[0]
        else:
            return []