from lib.api import MetroApi, STOP_DESCRIPTIONS, SCHEDULE
from datetime import datetime

class BusRoute:
    api: MetroApi = MetroApi()
    def __init__(self, route_id):
        """
        args:
        - route_id - metro transit route id. Can be found in `routes.txt`
        """
        self.route_id = str(route_id)
        self.schedule = {}
        
          

    def route_departures(self) -> dict[tuple[str, str], tuple[datetime, datetime]]:
        """
        realtime arrival info for a given bus route
        args: none
        returns:
        - dictionary of (trip_id, stop_id) -> (expected_departure, actual_departure)
        """

        updates: int = self.api.gtfs_feed()

        for entity in updates.entity:
            if entity.trip_update.trip.route_id != self.route_id:
                continue
        
            for delay in entity.trip_update.stop_time_update:
                key = (entity.trip_update.trip.trip_id, delay.stop_id)
                if key not in self.schedule: # check whether this update even applies
                    continue
                expected = self.schedule[key][0]
                self.schedule.update({key : (SCHEDULE[key], datetime.fromtimestamp(delay.departure.tim)) })

        """
        for stop in self.stops.values(): # pulls descriptions
            
            stop_id = STOP_DESCRIPTIONS.get(stop, None)
      
            if stop_id:
                res = self.api.departures(stop_id)
             
                for departure in res:
                    ident = (departure["trip_id"], stop_id)
                    expected_departure = SCHEDULE.get(ident, None)
                    if expected_departure and departure["route_id"] == self.route_id:
              
                        arrival_times = (expected_departure.timestamp(), datetime.fromtimestamp(departure["departure_time"]).timestamp())
                        schedule[ident] = arrival_times
        """
        return self.schedule

                