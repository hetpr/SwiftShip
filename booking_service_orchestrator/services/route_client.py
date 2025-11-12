import os
import requests
from dotenv import load_dotenv

load_dotenv()

ROUTE_SERVICE_URL = os.getenv("ROUTE_SERVICE_BASE") + "/optimal_route"

def get_best_route(source, destination):
    params = {"source": source, "destination": destination}
    try:
        r = requests.get(ROUTE_SERVICE_URL, params=params)
        data = r.json()
        return data.get("best_route"), data.get("total_distance_km")
    except:
        return None, None