import os
import requests
from dotenv import load_dotenv

load_dotenv()

ETA_SERVICE_URL = os.getenv("ETA_SERVICE_BASE") + "/predict_eta"

def get_eta(distance_km, priority="standard"):
    params = {"distance": distance_km, "priority": priority}
    try:
        r = requests.get(ETA_SERVICE_URL, params=params)
        return r.json().get("eta", "Unavailable")
    except:
        return "ETA Service Unavailable"