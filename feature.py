from google.transit import gtfs_realtime_pb2
from requests import get

feed = gtfs_realtime_pb2.FeedMessage()
response = get('https://svc.metrotransit.org/mtgtfs/vehiclepositions.pb')

feed.ParseFromString(response.content)

print(feed)
