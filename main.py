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


eline = BusRoute('925')
stop_ids = eline.stops()
found_stops = []
for i in range(10):
    stop_id = lib.api.STOP_DESCRIPTION.get(stop_ids[i], None)
    print('done')
    if stop_id:
        found_stops.append(stop_id)

stops: list[BusStop] = [BusStop(id) for id in found_stops]
print(stops)
for i in range(3):
    print(stops[i].departures)
# eline route_id: 925


