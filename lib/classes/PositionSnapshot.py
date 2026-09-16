from datetime import datetime

class PositionSnapshot:
    def __init__(self,route_id, trip_id, destination_stop_id, expected: int,timestamp: float, lat: float, lon: float, direction_id: int):
        self.route_id = route_id
        self.trip_id = trip_id
        self.destination_stop_id = destination_stop_id
        self.expected = datetime.fromtimestamp(expected)
        self.timestamp = datetime.fromtimestamp(timestamp)
        self.lat = lat
        self.lon = lon
        self.direction_id = direction_id