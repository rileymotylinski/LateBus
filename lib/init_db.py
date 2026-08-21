import sqlite3
import csv

"""
purpose: to restore a backup of a database should the data get screwed up
"""

lines = []
with open("backup.csv", "r") as f:
    reader = csv.reader(f)

    next(reader)

    for line in reader:
        lines.append(line)

con = sqlite3.connect('bus.db')

cur = con.cursor()

cur.execute("""
        CREATE TABLE IF NOT EXISTS departures(
            trip_id TEXT,
            route_id TEXT,
            stop_id TEXT,
            expected INTEGER,
            actual INTEGER,
            date  TEXT,
            PRIMARY KEY (trip_id, route_id, stop_id, date)
        )
    """)

cur.executemany("""
        INSERT OR REPLACE INTO departures (trip_id, route_id, stop_id, expected, actual, date)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT (trip_id, route_id, stop_id, date) DO UPDATE SET
            expected = excluded.expected,
            actual = excluded.actual
    """, lines)
con.commit()
cur.close()