import os
import requests
from dotenv import load_dotenv
load_dotenv()

BASE_URL = os.getenv("ROUTE_SERVICE_BASE")

def get_routes():
    return requests.get(f"{BASE_URL}/routes").json()

def get_route(route_id):
    return requests.get(f"{BASE_URL}/routes/{route_id}").json()

def add_route(source, destination, distance):
    payload = {"source": source, "destination": destination, "distance_km": distance}
    return requests.post(f"{BASE_URL}/routes", json=payload).json()

def update_route(route_id, source, destination, distance):
    payload = {"source": source, "destination": destination, "distance_km": distance}
    return requests.put(f"{BASE_URL}/routes/{route_id}", json=payload).json()

def delete_route(route_id):
    return requests.delete(f"{BASE_URL}/routes/{route_id}").json()