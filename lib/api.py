from requests import get



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
        self._base_url = "https://svc.metrotransit.org/nextrip"
        
    def routes(self):
        return get(self._base_url + "/routes").json()

    def directions(self, route_id):
        return get(self._base_url + f"/directions/{route_id}").json()

    def stops(self,route_id, direction_id) -> list[str]:
        return [s["place_code"] for s in get(self._base_url + f"/stops/{route_id}/{direction_id}").json()]

    def get_route_ids(self):
        return [r["route_id"] for r in self.routes()]
        
ROUTE_IDS = MetroApi().get_route_ids()



        
