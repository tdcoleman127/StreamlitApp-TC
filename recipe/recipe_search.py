import requests
import streamlit as st

from dotenv import load_dotenv
import os
from spoonacular_api import call_spoonacular_api

load_dotenv()  # take environment variables from .env

API_KEY = os.getenv("SPOONACULAR_API_KEY")

# Helper function to make API requests with error handling
def call_spoonacular_api(endpoint, params=None):
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
        response.raise_for_status()  # Will raise an exception for 4xx/5xx responses
        return response.json()

    except requests.exceptions.HTTPError as e:
        status_code = response.status_code
        if status_code == 401:
            st.error("Unauthorized: Your API key may be invalid or expired.")
        elif status_code == 402:
            st.error("Payment Required: Subscription may have expired.")
        elif status_code == 429:
            st.error("Rate Limit Exceeded: Too many requests.")
        else:
            st.error(f"HTTP Error {status_code}: {response.text}")
        return None

    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")
        return None


# Function to fetch recipes based on ingredients
def get_recipes_by_ingredients(ingredients):
    params = {
        "ingredients": ",".join(ingredients),
        "number": 5,
        "ranking": 1,
        "ignorePantry": True
    }
    return call_spoonacular_api("recipes/findByIngredients", params)


# Function to fetch full recipe information based on recipe ID
def get_recipe_info(recipe_id):
    params = {}
    return call_spoonacular_api(f"recipes/{recipe_id}/information", params)


# Main interaction function
def run_recipe_app():
    # User input: ingredients list
    ingredients_input = st.text_input("Enter ingredients below separated by commas (an example is given)", "chicken, rice, tomatoes")
    ingredients_list = [i.strip() for i in ingredients_input.split(",") if i.strip()]

    if not ingredients_list:
        st.warning("Please enter at least one ingredient.")
        return

    # Fetch basic recipe matches
    recipes = get_recipes_by_ingredients(ingredients_list)

    if recipes:
        # Display list of recipe titles and allow user to select one
        titles = [r["title"] for r in recipes]
        selected = st.selectbox("Select a recipe to view details", titles)
        selected_recipe = next(r for r in recipes if r["title"] == selected)

        # Display recipe image and summary
        st.image(selected_recipe["image"], width=250)
        st.markdown(f"**Used ingredients**: {selected_recipe['usedIngredientCount']}")
        st.markdown(f"**Missing ingredients**: {selected_recipe['missedIngredientCount']}")
        st.markdown(f"**Likes**: {selected_recipe.get('likes', 0)}")

        # Fetch full recipe details when user clicks "View Full Recipe"
        if st.button("View Full Recipe"):
            info = get_recipe_info(selected_recipe["id"])
            if info:  # Check if the info is successfully fetched
                st.subheader(info["title"])
                st.image(info["image"], width=300)
                st.markdown(f"**Ready in**: {info['readyInMinutes']} minutes")
                st.markdown(f"**Servings**: {info['servings']}")
                st.markdown("### Summary")
                st.markdown(info["summary"], unsafe_allow_html=True)
                st.markdown("### Instructions")
                st.markdown(info["instructions"] or "No instructions provided.")
                st.markdown(f"[Source]({info['sourceUrl']})")
        #Random recipe coming soon
    else:
        st.warning("No recipes found.")
