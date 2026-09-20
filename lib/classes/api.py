from requests import get, Response
from google.transit import gtfs_realtime_pb2


"""
    purpose: handles ALL parsing/calling of data from api
    - rate limiting
        - using rate limit library
    - easily adding endpoints
        - these will be hardcoded into the class

    - handling response codes
        - try catch blocks...on what?
    - data validation
        - custom solution
"""

class MetroApi():
    def __init__(self):
        self._base_url: str = "https://svc.metrotransit.org/nextrip"
        self.gtfs_feed = {}
        self.position_feed = None

    def _get_handler(self,url: str) -> Response | None:
        """
        purpose: return raw response from get call, "handles" if the request fails
        """
        res = get(url)

        if res.ok:
            return res
        else:
            
            print(f"failed with: {res.status_code}, {res.json()}")
            return None

    def update_gtfs_feed(self):

        self.gtfs_feed = gtfs_realtime_pb2.FeedMessage()
        response = self._get_handler('https://svc.metrotransit.org/mtgtfs/tripupdates.pb')
        if response:
            self.gtfs_feed.ParseFromString(response.content)

    def update_position_feed(self):
        self.position_feed = gtfs_realtime_pb2.FeedMessage()
        response = self._get_handler('https://svc.metrotransit.org/mtgtfs/vehiclepositions.pb')
        if response:
            self.position_feed.ParseFromString(response.content)

    def directions(self, route_id: str) -> list[dict[str, int]]:
        res = self._get_handler(self._base_url + f"/directions/{route_id}")
        return res.json() if res else [{}]
    
    def stops(self,route_id: str) -> dict[int, list[dict[str,str]]]:
        res: dict[int, list[dict[str,str]]] = {}
        directions = self.directions(route_id)
        if not directions:
            return {}
        for direction in directions:
            if not direction:
                continue
            try:
                direction_id: int = direction["direction_id"]
            except:
                print(direction)
                continue
            stops_dir = self.stops_dir(route_id, str(direction_id))
            res[direction_id] = stops_dir
        return res
    def stops_dir(self,route_id: str, direction_id: str) -> list[dict[str,str]]:
        res = self._get_handler(self._base_url + f"/stops/{route_id}/{direction_id}")
        return res.json() if res else [{}]








        
