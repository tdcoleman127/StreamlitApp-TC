import streamlit as st
import random

st.set_page_config(page_title="What's in Your Fridge?", page_icon="🥦")

st.title("🥦 Recipe Generator Based on Ingredients")
st.write("Type a few ingredients you have, and I’ll find a recipe... or make one up!")

# --- Input Ingredients ---
ingredients_input = st.text_input("What ingredients do you have? (comma-separated)")
ingredients = [i.strip().lower() for i in ingredients_input.split(",") if i.strip()]

# --- Static Recipes Bank ---
recipes = {
    "pasta": {
        "ingredients": ["pasta", "tomato", "basil"],
        "instructions": "Boil pasta. Make a quick tomato sauce. Toss and serve with basil."
    },
    "omelette": {
        "ingredients": ["eggs", "cheese", "spinach"],
        "instructions": "Beat eggs, cook in a pan, and sprinkle in cheese and spinach before folding."
    },
    "stir fry": {
        "ingredients": ["rice", "soy sauce", "broccoli", "chicken"],
        "instructions": "Stir-fry chicken and veggies. Add soy sauce. Serve over rice."
    }
}

# --- Match Recipes ---
matched = None
for name, data in recipes.items():
    if any(item in ingredients for item in data["ingredients"]):
        matched = (name, data)
        break

# --- Output Recipe or Funny Version ---
if ingredients:
    if matched:
        st.subheader(f"🍽 You can make: {matched[0].title()}")
        st.write(matched[1]["instructions"])
    else:
        st.subheader("🤪 Fridge Clean-Out Mode Activated!")
        random_recipe = ", ".join(random.sample(ingredients, min(len(ingredients), 3)))
        weird_methods = [
            "deep-fry it in maple syrup", "bake it under the sun", 
            "blend it with soda", "cover it in cheese and hope for the best"
        ]
        st.write(f"Mix {random_recipe}, then {random.choice(weird_methods)}.")

# --- Feedback Section ---
st.markdown("---")
st.subheader("📝 What did you think of your recipe?")
rating = st.radio("Would you eat this?", ["😋 Absolutely", "🤔 Maybe", "😖 Never again"], horizontal=True)
comments = st.text_area("Leave a comment (optional):")

if st.button("Submit Feedback"):
    st.success("Thanks for your feedback!")
