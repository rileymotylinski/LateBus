from lib.classes.BusRoute import BusRoute
from lib.scripts.metro_constants import ROUTE_IDS, MetroApi, SCHEDULE
import os
import time
from datetime import datetime
import sqlite3
from lib.classes.PositionSnapshot import PositionSnapshot
from lib.scripts.init_db import init_bus_db

POLL_RATE = 5 # in seconds
DATABASE_NAME = "bus.db"
con = sqlite3.connect(DATABASE_NAME)


buses = [BusRoute(s) for s in ROUTE_IDS] 

dir = os.path.dirname(__file__)



def dump_positions(entries: list[PositionSnapshot]):
    init_bus_db()
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

            entries.append(PositionSnapshot(
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


