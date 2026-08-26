from google.transit import gtfs_realtime_pb2
from requests import get
from lib.api import MetroApi, STOP_DESCRIPTIONS

feed = gtfs_realtime_pb2.FeedMessage()
response = get('https://svc.metrotransit.org/mtgtfs/vehiclepositions.pb')

feed.ParseFromString(response.content)
api = MetroApi()


"""
get all vehicles
get what stop each vehicle is going to 
get the route shape
get distance to next stop
"""
for entity in feed.entity:

    next_stop_id = entity.vehicle.stop_id
    trip_id = entity.vehicle.trip.trip_id
    route_id = entity.vehicle.trip.route_id
    direction_id = entity.vehicle.trip.direction_id

    if not next_stop_id:
        continue

    
       

print(stops)
 

print(api.stops("925"))


