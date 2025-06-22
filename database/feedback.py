from .supabase_client import SUPABASE_URL, HEADERS
import requests

def insert_feedback(name, used_before, rating, favorites, comments):
    data = {
        "name": name,
        "used_before": used_before,
        "rating": rating,
        "favorites": favorites,
        "comments": comments
    }
    response = requests.post(
        f"{SUPABASE_URL}/rest/v1/feedback",
        headers=HEADERS,
        json=data
    )
    return response.status_code, response.text

def get_feedback():
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/feedback?select=*",
        headers=HEADERS
    )
    return response.json()

def clear_feedback():
    response = requests.delete(
        f"{SUPABASE_URL}/rest/v1/feedback?name=neq.null",
        headers=HEADERS
    )
    return response.status_code, response.text
