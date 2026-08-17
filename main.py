from lib.BusRoute import BusRoute
import os
import time
from datetime import datetime
import sqlite3

POLL_RATE = 15 # in seconds
DATABASE_NAME = "bus.db"
con = sqlite3.connect(DATABASE_NAME)

current_schedule: dict = {}

target_route = '925'
eline = BusRoute(target_route) # route_id for e line

dir = os.path.dirname(__file__)

def _init_bus_db():
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS departures(
            trip_id TEXT,
            route_id TEXT,
            expected INTEGER,
            actual INTEGER,
            PRIMARY KEY (trip_id, route_id)
        )
    """)
    cur.close()

def dump(schedule: dict[tuple[str, str], tuple[datetime, datetime]]):
    _init_bus_db()
    cur = con.cursor()
    schedule = [(s[0], s[1], schedule[s][0], schedule[s][1]) for s in schedule]
    print(schedule[0][2])
    cur.executemany("""
        INSERT OR REPLACE INTO departures (trip_id, route_id, expected, actual)
        VALUES (?, ?, ?, ?)
        ON CONFLICT (trip_id, route_id) DO UPDATE SET
            expected = excluded.expected,
            actual = excluded.actual
    """, schedule)
    cur.close()

        
failed_attempts = 0

while True:
  
    try:
        current_schedule.update(eline.route_departures())
        
        dump(current_schedule)
        print("wrote out schedule")
        time.sleep(POLL_RATE)
        failed_attempts = 0
    except Exception as e:
        print(f"{e}")
        if failed_attempts > 4:
            print("failed to many times. exiting scripts")
            break
        else:
            failed_attempts += 1
            
            time.sleep(POLL_RATE*4)



