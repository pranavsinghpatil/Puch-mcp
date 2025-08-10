# app/services/locality_service.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

def get_nearby_places(dish, city):
    query = f"{dish} in {city}"
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&key={API_KEY}"
    response = requests.get(url).json()

    if "results" not in response:
        return []

    results = []
    for place in response["results"][:5]:  # Limit to top 5
        results.append({
            "name": place["name"],
            "address": place.get("formatted_address", "Address not available"),
            "rating": place.get("rating", "N/A"),
            "maps_url": f"https://www.google.com/maps/place/?q=place_id:{place['place_id']}"
        })
    return results
