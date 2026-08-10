from lib.BusStop import BusStop
import lib.api
import os
import csv
from datetime import datetime


stops: dict[str, BusStop] = {}

for id in lib.api.STOP_IDS:
    stops[id] = BusStop(id)

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

def amend_schedule(real_schedule: list[BusStop], expected_schedule: dict[tuple, datetime]):
    """
    1. look at each departure at a given bus stop
    2. Did it arrive on time?
    -> query the expected schedule for the real time
    """

    for stop in real_schedule:
        
        for departure in real_schedule[stop].departures:
            real_time = datetime.fromtimestamp(departure["departure_time"])
            query = (departure["trip_id"], str(departure["stop_id"]))
            expected_time = expected_schedule[query]
            print(real_time - expected_time)

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

for i in range(100):
    stops[lib.api.STOP_IDS[i]].update_departures()

amend_schedule(stops,scheduled_arrivals)


