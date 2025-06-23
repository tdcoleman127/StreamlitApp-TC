import streamlit as st
import requests

st.title("🥘 Find Recipes by Ingredients (TheMealDB)")
st.write("Enter up to 3 ingredients to get real recipes. Choose one to see full instructions!")

# --- Input Ingredients ---
ingredient1 = st.text_input("Ingredient 1")
ingredient2 = st.text_input("Ingredient 2")
ingredient3 = st.text_input("Ingredient 3")

ingredients = [i.strip().lower() for i in [ingredient1, ingredient2, ingredient3] if i.strip()]

if ingredients:
    # Filter meals by first ingredient
    base_url = "https://www.themealdb.com/api/json/v1/1/filter.php?i="
    response = requests.get(base_url + ingredients[0])
    data = response.json()

    if not data["meals"]:
        st.error("No meals found with that ingredient.")
    else:
        # Filter by the other ingredients manually
        filtered_meals = data["meals"]
        for ing in ingredients[1:]:
            next_response = requests.get(base_url + ing)
            next_data = next_response.json()
            if next_data["meals"]:
                ids = set([meal["idMeal"] for meal in next_data["meals"]])
                filtered_meals = [meal for meal in filtered_meals if meal["idMeal"] in ids]
            else:
                filtered_meals = []

        if not filtered_meals:
            st.warning("No recipes found that match all ingredients.")
        else:
            # Let user pick from matching meals
            meal_names = {meal["strMeal"]: meal["idMeal"] for meal in filtered_meals}
            selected_meal_name = st.selectbox("Choose a matching recipe:", list(meal_names.keys()))
            selected_id = meal_names[selected_meal_name]

            # Fetch full meal details
            detail_url = f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={selected_id}"
            detail_data = requests.get(detail_url).json()["meals"][0]

            # Display full recipe
            st.subheader(detail_data["strMeal"])
            st.image(detail_data["strMealThumb"])
            st.markdown(f"**Category:** {detail_data['strCategory']}")
            st.markdown(f"**Cuisine:** {detail_data['strArea']}")
            st.markdown("### Instructions")
            st.write(detail_data["strInstructions"])
            if detail_data["strYoutube"]:
                st.markdown(f"[Watch on YouTube]({detail_data['strYoutube']})")
