from google.transit import gtfs_realtime_pb2
from requests import get
from lib.api import MetroApi

feed = gtfs_realtime_pb2.FeedMessage()
response = get('https://svc.metrotransit.org/mtgtfs/vehiclepositions.pb')

feed.ParseFromString(response.content)

print(feed)

"""
get all vehicles
get what stop each vehicle is going to 
get the route shape
get distance to next stop
"""
for entity in feed.entity:
    print(entity)
    next_stop = entity.vehicle.stop_id
    trip_id = entity.vehicle.trip.trip_id
    route_id = entity.vehicle.trip.route_id

    if not next_stop:
        continue
    print(next_stop)



