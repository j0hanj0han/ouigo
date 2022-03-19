import requests
import pprint
from loguru import logger


class OuiGoTracker:

    def __init__(self, token):
        self.token = token
        self.base_url = "https://api.sncf.com/v1"

    
    def _make_requests(self, method, endpoint):
        try:
            url = self.base_url + endpoint
            header = {'Authorization': 'Bearer ' + self.token}
            resp =  requests.request(method, url, auth=(self.token, None))
            if resp.ok:
                logger.info(f"HTTP Status code {resp.status_code}")
                return resp.json()
            else:
                raise Exception
        except Exception:
            logger.error(f"ERROR while requesting {url}")
            logger.error(f"HTTP Status code {resp.status_code}")
            pass

    def get_transport_modes(self):
        logger.info("Getting Transport Mode")
        method = "GET"
        endpoint = "/coverage/sncf/commercial_modes"
        result =  self._make_requests(method, endpoint)
        pprint.pprint(result)
        return result

    def get_journeys(self, city1, city2, date):
        logger.info("Getting Journeys")
        method = "GET"
        endpoint = f"/coverage/sncf/journeys?from={city1}&to={city2}&datetime={date}"
        result =  self._make_requests(method, endpoint)

        next_departure = [r["departure_date_time"] for r in result["journeys"]]
        logger.info(f"Next departure  {next_departure}")
        first_result = result["journeys"][0]
        with open("sample.json", "w") as outfile:
            outfile.write(str(first_result))

        return result


    def write_in_csv(self, data):
        pass

    
if __name__ == "__main__":
    token = ""

    ouigo =  OuiGoTracker(token)
    #ouigo.get_transport_modes()


    paris = "admin:fr:75056"
    mtp = "admin:fr:69123"
    date = "20220319T082817"
    ouigo.get_journeys(mtp, paris, date)

#     Le détail des modes de transport couvert par l’API 
# GET https://api.sncf.com/v1/coverage/sncf/commercial_modes 

# Itinéraires entre Paris et Lyon 
# GET https://api.sncf.com/v1/coverage/sncf/journeys?from=admin:fr:75056&to=admin:fr:69123&datetime=20220319T082817 

# Prochains départs à Montparnasse 
# GET https://api.sncf.com/v1/coverage/sncf/stop_areas/stop_area:SNCF:87391003/departures?datetime=20220319T082817 

