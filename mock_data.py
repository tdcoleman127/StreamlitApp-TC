# mock_data.py

mock_recipe_response = [
    {
        "id": 10101,
        "title": "Grilled Chicken and Rice Bowl",
        "image": "https://via.placeholder.com/312x231.png?text=Chicken+Rice+Bowl",
        "imageType": "jpg",
        "usedIngredientCount": 2,
        "missedIngredientCount": 1,
        "likes": 134
    },
    {
        "id": 20202,
        "title": "Tomato Basil Pasta",
        "image": "https://via.placeholder.com/312x231.png?text=Tomato+Basil+Pasta",
        "imageType": "jpg",
        "usedIngredientCount": 1,
        "missedIngredientCount": 2,
        "likes": 198
    },
    {
        "id": 30303,
        "title": "Veggie Stir Fry",
        "image": "https://via.placeholder.com/312x231.png?text=Veggie+Stir+Fry",
        "imageType": "jpg",
        "usedIngredientCount": 3,
        "missedIngredientCount": 0,
        "likes": 212
    }
]

mock_recipe_info = {
    "id": 10101,
    "title": "Grilled Chicken and Rice Bowl",
    "image": "https://via.placeholder.com/480x360.png?text=Full+Recipe+Image",
    "readyInMinutes": 35,
    "servings": 2,
    "summary": (
        "A mock recipe of grilled chicken over a bed of fluffy rice, "
        "perfect for development environments. Packed with protein and ready in just over 30 minutes."
    ),
    "instructions": (
        "1. Heat grill or skillet over medium heat.\n"
        "2. Season chicken with salt, pepper, and paprika.\n"
        "3. Cook chicken until browned and fully cooked.\n"
        "4. Serve over cooked rice with chopped herbs and optional sauce."
    ),
    "sourceUrl": "https://example.com/mock-recipe"
}
