from lib.BusRoute import BusRoute
import os
import time
from datetime import datetime
import csv
from tempfile import NamedTemporaryFile
import shutil


POLL_RATE = 15 # in seconds
TEMP_FILE = "temp.txt"
OUTPUT_FILE = "out.txt"


current_schedule: dict = {}

target_route = '925'
eline = BusRoute(target_route) # route_id for e line

dir = os.path.dirname(__file__)
old = os.path.join(dir, OUTPUT_FILE)
new = os.path.join(dir, TEMP_FILE)




def dump(schedule: dict[tuple[str, str], tuple[datetime, datetime]]):
   

    with open(old, "r") as oldfile, open(new, "w") as newfile:
        csvwriter = csv.DictWriter(newfile, ["trip_id", "stop_id", "expected_departure", "actual_departure"])
        csvreader = csv.reader(oldfile)


        for row in csvreader:
            key = (row[0], row[1])
            # update existing entries
            if key in schedule:
                res = schedule.pop(key)
                csvwriter.writerow({"trip_id" : row[0], "stop_id" : row[1], "expected_departure" : res[0], "actual_departure" : res[1]})
            # rewrite old entries
            else:
                csvwriter.writerow({"trip_id" : row[0], "stop_id" : row[1], "expected_departure" : row[2], "actual_departure" : row[3]})
        
        # add new entires
        for new_entry in schedule:
            csvwriter.writerow({"trip_id" : new_entry[0], "stop_id" : new_entry[1], "expected_departure" : schedule[new_entry][0], "actual_departure" : schedule[new_entry][1]})
   
    shutil.move(TEMP_FILE, OUTPUT_FILE)
        


while True:
    try:
        current_schedule.update(eline.route_departures())
        
        dump(current_schedule)
        print("wrote out schedule")
        time.sleep(POLL_RATE)
    except:
        time.sleep(POLL_RATE*4)


