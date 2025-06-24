# recipe_api.py
import requests

API_KEY = "YOUR_SPOONACULAR_API_KEY"  # Replace with your actual key

def find_recipes_by_ingredients(ingredients_list, count=5):
    url = "https://api.spoonacular.com/recipes/findByIngredients"
    params = {
        "ingredients": ",".join(ingredients_list),
        "number": count,
        "apiKey": API_KEY
    }
    return requests.get(url, params=params).json()

def get_recipe_details(recipe_id):
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
    params = {"apiKey": API_KEY}
    return requests.get(url, params=params).json()
