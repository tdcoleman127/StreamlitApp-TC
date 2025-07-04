# database.py

import requests
import streamlit as st

SUPABASE_URL = st.secrets["supabase"]["url"]
SUPABASE_KEY = st.secrets["supabase"]["key"]
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

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
