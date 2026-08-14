from lib.BusRoute import BusRoute
import os
import time
from datetime import datetime
import csv

dir = os.path.dirname(__file__)
out = os.path.join(dir,"out.txt")
POLL_RATE = 15 # in seconds

current_schedule: dict = {}

target_route = '925'
eline = BusRoute(target_route) # route_id for e line

def dump(schedule: dict[tuple[str, str], tuple[datetime, datetime]]):
    with open(out, "w") as csvfile:
        csvwriter = csv.writer(csvfile)
        for k in schedule:
            # trip_id, stop_id, expected_departure, actual_departure
            csvwriter.writerow([k[0],k[1], schedule[k][0],schedule[k][1]])
        csvfile.close()


while True:
    current_schedule.update(eline.route_departures())
    dump(current_schedule)
    print("wrote out schedule")
    time.sleep(POLL_RATE)


