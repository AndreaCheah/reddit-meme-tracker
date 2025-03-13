import requests
from typing import List, Dict

API_URL = "http://127.0.0.1:8000/top-memes"

def fetch_memes() -> List[Dict]:
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as error:
        print(f"Error fetching memes from API: {error}")
        return []
