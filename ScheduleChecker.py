from datetime import datetime
from lib.scripts.init_db import init_bus_db
from lib.classes.api import MetroApi
from lib.scripts.metro_constants import ROUTE_IDS
from lib.classes.BusRoute import BusRoute
import sqlite3
import time


POLL_RATE = 5 # in seconds
DATABASE_NAME = "bus.db"
con = sqlite3.connect(DATABASE_NAME)
init_bus_db(con)

def dump(actual_schedule: dict[tuple[str, str], float], expected_schedule: dict[tuple[str, str], datetime], route_id):
    init_bus_db(con)
    cur = con.cursor()
    # TODO: We should only be dumping ON the date the bus stop is happening, right?

    schedule = [(s[0],route_id, s[1], actual_schedule[s], expected_schedule[s], datetime.fromtimestamp(actual_schedule[s]).date().isoformat()) for s in actual_schedule]

    cur.executemany("""
        INSERT OR REPLACE INTO departures (trip_id, route_id, stop_id, expected, actual, date)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT (trip_id, route_id, stop_id, date) DO UPDATE SET
            expected = excluded.expected,
            actual = excluded.actual
    """, schedule)
    con.commit()
    cur.close()

api = MetroApi()
buses = [BusRoute(s) for s in ROUTE_IDS] 

while True: 
    api.update_gtfs_feed()
    
    if api.gtfs_feed:
        for bus in buses:
            try:
                bus.update_route_departures(api.gtfs_feed)
                dump(bus.actual_schedule, bus.expected_schedule, bus.route_id)
        
                failed_attempts = 0
            except Exception as e:
                print(f"{e}")
                if failed_attempts > 4:
                    print("failed to many times. exiting scripts")
                    break
                else:
                    failed_attempts += 1
                    
                    time.sleep(POLL_RATE*4)
    print("wrote out schedule")
    time.sleep(POLL_RATE)