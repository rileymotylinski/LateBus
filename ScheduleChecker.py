from datetime import datetime
from lib.scripts.init_db import init_bus_db

def dump(actual_schedule: dict[tuple[str, str], float], expected_schedule: dict[tuple[str, str], datetime], route_id):
    init_bus_db()
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