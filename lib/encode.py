from lib.api import MAX_ROUTE_ID

class Departure:
    def __init__(self, trip_id, route_id, stop_id, expected, actual, date):
        # database schema
        self.trip_id = trip_id
        self.route_id = route_id
        self.stop_id = stop_id
        self.expected = expected
        self.actual = actual
        self.date = date

def one_hot_encode(route_id):
    vec = [0] * (MAX_ROUTE_ID + 1)
    vec[route_id] = 1
    return vec


