from lib.BusStop import BusStop
import lib.api

stops: list[BusStop] = []


for id in lib.api.STOP_IDS:
    stops.append(BusStop(id))

for s in stops:
    print(s.next_departure())

