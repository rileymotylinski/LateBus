from lib.api import MetroApi, SCHEDULE
from datetime import datetime

class BusRoute:
    api: MetroApi = MetroApi()
    def __init__(self, route_id):
        """
        args:
        - route_id - metro transit route id. Can be found in `routes.txt`
        """
        self.route_id = str(route_id)
        self.expected_schedule = SCHEDULE[route_id]
        self.actual_schedule = {} # only gather data for stops we've colelcted while running.

    def update_route_departures(self, updates) -> dict[tuple[str, str], datetime]:
        """
        realtime arrival info for a given bus route
        args: none
        returns:
        - dictionary of (trip_id, stop_id) -> actual_departure
        """
     
        for entity in updates.entity:
            
            if entity.trip_update.trip.route_id != self.route_id:
                continue
            
            for delay in entity.trip_update.stop_time_update:
                key = (entity.trip_update.trip.trip_id, delay.stop_id)
             
                if key not in self.expected_schedule or self.expected_schedule[key] == delay.departure.time: # check whether this update even applies
                    continue
                self.actual_schedule[key] = delay.departure.time

        return self.actual_schedule

                