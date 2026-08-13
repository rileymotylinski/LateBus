from lib.BusStop import BusStop
from lib.BusRoute import BusRoute
import lib.api
import os
import csv
from datetime import datetime

stops: dict[str, BusStop] = {}

dir = os.path.dirname(__file__)
stop_times = os.path.join(dir,"lib", "Schedule","stop_times.csv")
scheduled_arrivals = {}

def parse_time(time: str):
    """
    time - HH:MM:SS format
    """
    parts = time.split(":")

    if len(parts) != 3:
        print("improper time format")
        return
    return (int(parts[0]),int(parts[1]),int(parts[2]))

total_invalid = 0
with open (stop_times, "r",  newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    
    for r in reader:
        trip_id = r[0]
        hour, min, second = parse_time(r[2])
        stop_id = r[3]
        
        if (hour > 23):
            total_invalid += 1
            continue
       
        expected = datetime.today().replace(hour=hour,minute=min, second=second)
        scheduled_arrivals[(trip_id,stop_id)] = expected
print(f"found {total_invalid} invalid times")

target_route = '925'
eline = BusRoute(target_route) # route_id for e line
print(eline.stops)
eline.route_departures()



