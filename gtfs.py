from google.transit import gtfs_realtime_pb2
import requests


feed = gtfs_realtime_pb2.FeedMessage()
response = requests.get('https://svc.metrotransit.org/mtgtfs/tripupdates.pb')
feed.ParseFromString(response.content)
for entity in feed.entity:
 
    print((entity.trip_update.trip.trip_id, entity.trip_update.trip.route_id))
    for delay in entity.trip_update.stop_time_update:
        print(delay)