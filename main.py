from lib.BusRoute import BusRoute
import os

dir = os.path.dirname(__file__)
out = os.path.join(dir,"out.txt")

current_schedule: dict = {}

target_route = '925'
eline = BusRoute(target_route) # route_id for e line

current_schedule.update(eline.route_departures())
print(current_schedule)


