import streamlit as st
import requests

from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env

API_KEY = os.getenv("SPOONACULAR_API_KEY")

def run_recipe_app():
    st.title("🥦 Welcome to RecipeTent™!")
    st.warning("🛠️ This app is currently under development")
    st.image("assets/mylogo.png", width=200)
    st.subheader("🍳'Cook with confidence!'")
    st.subheader("Type in a few ingredients, and get a recipe from them!")

    # User input
    ingredients_input = st.text_input("Enter ingredients below separated by commas (an example is given)", "chicken, rice, tomatoes")
    ingredients_list = [i.strip() for i in ingredients_input.split(",") if i.strip()]

    if not ingredients_list:
        st.warning("Please enter at least one ingredient.")
        return

    # Fetch basic recipe matches
    def get_recipes_by_ingredients(ingredients):
        url = "https://api.spoonacular.com/recipes/findByIngredients"
        params = {
            "ingredients": ",".join(ingredients),
            "number": 5,
            "ranking": 1,
            "ignorePantry": True,
            "apiKey": API_KEY
        }
        response = requests.get(url, params=params)
        return response.json()

    # Fetch full details
    def get_recipe_info(recipe_id):
        url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
        params = {"apiKey": API_KEY}
        response = requests.get(url, params=params)
        return response.json()

    # Main interaction
    recipes = get_recipes_by_ingredients(ingredients_list)

    if recipes:
        titles = [r["title"] for r in recipes]
        selected = st.selectbox("Select a recipe to view details", titles)
        selected_recipe = next(r for r in recipes if r["title"] == selected)

        st.image(selected_recipe["image"], width=250)
        st.markdown(f"**Used ingredients**: {selected_recipe['usedIngredientCount']}")
        st.markdown(f"**Missing ingredients**: {selected_recipe['missedIngredientCount']}")
        st.markdown(f"**Likes**: {selected_recipe.get('likes', 0)}")

        if st.button("View Full Recipe"):
            info = get_recipe_info(selected_recipe["id"])
            st.subheader(info["title"])
            st.image(info["image"], width=300)
            st.markdown(f"**Ready in**: {info['readyInMinutes']} minutes")
            st.markdown(f"**Servings**: {info['servings']}")
            st.markdown("### Summary")
            st.markdown(info["summary"], unsafe_allow_html=True)
            st.markdown("### Instructions")
            st.markdown(info["instructions"] or "No instructions provided.")
            st.markdown(f"[Source]({info['sourceUrl']})")
    else:
        st.warning("No recipes found.")