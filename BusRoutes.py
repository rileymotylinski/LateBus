from lib.bus_route import BusStop
import lib.api

routes = []

print(lib.api.STOP_IDS)
for id in lib.api.STOP_IDS:
    routes.append(BusStop(id))

