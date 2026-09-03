from lib.BusRoute import BusRoute
from lib.api import ROUTE_IDS, MetroApi, SCHEDULE
import os
import time
from datetime import datetime
import sqlite3
from lib.encode import Bus

POLL_RATE = 5 # in seconds
DATABASE_NAME = "bus.db"
con = sqlite3.connect(DATABASE_NAME)


buses = [BusRoute(s) for s in ROUTE_IDS] 

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

    cur.execute("""
            CREATE TABLE IF NOT EXISTS positions(
                route_id TEXT,
                trip_id TEXT,
                destination_stop_id TEXT,
                expected INTEGER,
                timestamp INTEGER,
                lat FLOAT,
                lon FLOAT,
                direction_id INTEGER
            )
        """)
    cur.close()



def dump(actual_schedule: dict[tuple[str, str], datetime], expected_schedule: dict[tuple[str, str], datetime], route_id):
    _init_bus_db()
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

def dump_positions(entries: list[Bus]):
    _init_bus_db()
    cur = con.cursor()
    rows = [[str(b.route_id),
            str(b.trip_id),
            str(b.destination_stop_id),
            int(b.expected.timestamp()),
            int(b.timestamp.timestamp()),
            float(b.lat),
            float(b.lon),
            int(b.direction_id)] for b in entries]
    cur.executemany("""
            INSERT OR REPLACE INTO positions (route_id, trip_id, destination_stop_id, expected, timestamp, lat, lon, direction_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, rows)
    con.commit()
    cur.close()
        
failed_attempts = 0

api = MetroApi()


while True:
    api.update_position_feed()
    entries = []
    if api.position_feed:
        
        for entity in api.position_feed.entity:
            route_id = entity.vehicle.trip.route_id
            trip_id = entity.vehicle.trip.trip_id
            stop_id = entity.vehicle.stop_id
            if stop_id == None or stop_id == '':
                # a lot of them are missing stop_ids for some reason?
                continue
            latitude = entity.vehicle.position.latitude
            longitude = entity.vehicle.position.longitude
            direction_id = entity.vehicle.trip.direction_id

            if not (route_id 
                    or trip_id 
                    or stop_id 
                    or latitude 
                    or longitude
                    or direction_id):
                print("missing required field")
                continue

            expected_arrival = SCHEDULE.get(route_id, None)
            if not expected_arrival or expected_arrival == {}:
                print("unable to locate in schedule")
                continue
            expected_arrival = expected_arrival.get((trip_id, stop_id), None)
            if not expected_arrival or expected_arrival == {}:
                print("unable to locate in schedule")
                continue

            entries.append(Bus(
                    route_id,
                    trip_id,
                    stop_id,
                    expected_arrival,
                    datetime.now().timestamp(),
                    latitude,
                    longitude,
                    direction_id
                ))
            
        dump_positions(entries)
    print("wrote out schedule")
    time.sleep(POLL_RATE)


