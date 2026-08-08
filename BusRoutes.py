from lib.BusStop import BusStop
import lib.api
import os
import csv
from datetime import datetime

stops: list[BusStop] = []


for id in lib.api.STOP_IDS:
    stops.append(BusStop(id))

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
       
        expected = datetime.today().replace(hour=hour,minute=min, second=second, microsecond=0)
        scheduled_arrivals[expected] = (trip_id,stop_id)
print(f"found {total_invalid} invalid times")
arrivals = list(scheduled_arrivals.keys())
arrivals.sort()
print("sorted")

for s in stops:
    real_departure = s.next_departure()
    trip_id = real_departure.get("trip_id", None)
    if trip_id and real_departure["departure_text"] == "Due" and (trip_id,s.stop_id) in scheduled_arrivals:
        scheduled_arrival = scheduled_arrivals.get((trip_id,s.stop_id))
        
        print(f"left at: {datetime.fromtimestamp(real_departure["departure_time"])} expected: PLACEHOLDEr")


