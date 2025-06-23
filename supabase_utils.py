# supabase_utils.py
import requests
from datetime import datetime
import streamlit as st

SUPABASE_URL = st.secrets["supabase"]["url"]
SUPABASE_KEY = st.secrets["supabase"]["key"]
TABLE_NAME = "recipe_feedback"

def log_recipe_feedback(ingredients, recipe_title, recipe_id):
    url = f"{SUPABASE_URL}/rest/v1/{TABLE_NAME}"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }

    data = {
        "ingredients_used": ingredients,
        "recipe_title": recipe_title,
        "recipe_id": recipe_id,
        "timestamp": datetime.utcnow().isoformat()
    }

    response = requests.post(url, json=data, headers=headers)
    return response
