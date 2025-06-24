import requests
import streamlit as st

def call_spoonacular_api(endpoint: str, params: dict = None):
    API_KEY = st.secrets["SPOONACULAR_API_KEY"]
    BASE_URL = "https://api.spoonacular.com"
    headers = {"Content-Type": "application/json"}

    if not API_KEY:
        st.warning("Missing Spoonacular API key.")
        return None

    if params is None:
        params = {}
    params["apiKey"] = API_KEY

    try:
        response = requests.get(f"{BASE_URL}/{endpoint}", headers=headers, params=params)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.HTTPError as e:
        status_code = response.status_code
        if status_code == 401:
            st.error("Unauthorized: Your API key may be invalid or expired.")
        elif status_code == 402:
            st.error("Payment Required: Your subscription may have expired.")
        elif status_code == 429:
            st.error("Rate Limit Exceeded: You've made too many requests.")
        else:
            st.error(f"HTTP Error {status_code}: {response.text}")
        return None

    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")
        return None
