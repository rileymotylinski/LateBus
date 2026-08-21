from lib.BusRoute import BusRoute
import os
import time
from datetime import datetime
import sqlite3

POLL_RATE = 5 # in seconds
DATABASE_NAME = "bus.db"
con = sqlite3.connect(DATABASE_NAME)

target_routes = ['925', '901','905','120', '121']
buses = [BusRoute(s) for s in target_routes] 

dir = os.path.dirname(__file__)

def _init_bus_db():
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS departures(
            trip_id TEXT,
            route_id TEXT,
            stop_id TEXT,
            expected INTEGER,
            actual INTEGER,
            date TEXT,
            PRIMARY KEY (trip_id, route_id, stop_id, date)
        )
    """)
    cur.close()



def dump(actual_schedule: dict[tuple[str, str], datetime], expected_schedule: dict[tuple[str, str], datetime], route_id):
    _init_bus_db()
    cur = con.cursor()
    # TODO: We should only be dumping ON the date the bus stop is happening, right?

    schedule = [(s[0],route_id, s[1], actual_schedule[s], expected_schedule[s], datetime.fromtimestamp(actual_schedule[s]).date().isoformat()) for s in actual_schedule]
    print(len(schedule))
    cur.executemany("""
        INSERT OR REPLACE INTO departures (trip_id, route_id, stop_id, expected, actual, date)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT (trip_id, route_id, stop_id, date) DO UPDATE SET
            expected = excluded.expected,
            actual = excluded.actual
    """, schedule)
    con.commit()
    cur.close()

        
failed_attempts = 0

while True:
    for stop in buses:
        try:
            stop.update_route_departures()
            dump(stop.actual_schedule, stop.expected_schedule, stop.route_id)
            print("wrote out schedule")
            
            failed_attempts = 0
        except Exception as e:
            print(f"{e}")
            if failed_attempts > 4:
                print("failed to many times. exiting scripts")
                break
            else:
                failed_attempts += 1
                
                time.sleep(POLL_RATE*4)
    time.sleep(POLL_RATE)


