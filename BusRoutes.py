from lib.bus_route import BusRoute
import lib.api

routes = []

for id in lib.api.ROUTE_IDS:
    routes.append(BusRoute(id))

for r in routes:
    print(r.stops)