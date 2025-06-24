import requests
import streamlit as st
from spoonacular_api import call_spoonacular_api
from mock_data import mock_recipe_response, mock_recipe_info

API_KEY = st.secrets["SPOONACULAR_API_KEY"]
USE_MOCK_API = st.secrets.get("USE_MOCK_API", False)

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
    if USE_MOCK_API:
        return mock_recipe_response
    params = {
        "ingredients": ",".join(ingredients),
        "number": 5,
        "ranking": 1,
        "ignorePantry": True
    }
    return call_spoonacular_api("recipes/findByIngredients", params)


# Function to fetch full recipe information based on recipe ID
def get_recipe_info(recipe_id):
    if USE_MOCK_API:
        return mock_recipe_info
    params = {}
    return call_spoonacular_api(f"recipes/{recipe_id}/information", params)


# Main interaction function
def run_recipe_app():
    if USE_MOCK_API:
        st.info("🧪 Mock mode enabled – No real API calls are being made.")

    st.warning("🛠️ This app is currently under development")
    st.title("🥦 Welcome to RecipeTent™!")
    st.subheader("🍳'Cook with confidence!'")
    st.image("assets/mylogo.png", width=200)
    st.subheader("Type in a few ingredients, and get a recipe from them!")
    # User input: ingredients list
    ingredients_input = st.text_input("Enter ingredients below separated by commas (Ex. beans, greens, potatoes)")
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
