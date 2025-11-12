import os
import requests
from dotenv import load_dotenv
load_dotenv()

BASE_URL = os.getenv("ETA_SERVICE_BASE")

def get_eta_history():
    return requests.get(f"{BASE_URL}/history").json()

def add_eta_history(distance, days, priority, notes=""):
    payload = {
        "distance_km": distance,
        "actual_days": days,
        "priority": priority,
        "notes": notes
    }
    return requests.post(f"{BASE_URL}/history", json=payload).json()

def delete_eta_history(record_id):
    return requests.delete(f"{BASE_URL}/history/{record_id}").json()