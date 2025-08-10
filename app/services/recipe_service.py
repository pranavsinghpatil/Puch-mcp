# app/services/recipe_service.py
import sqlite3

def get_recipe_details(dish_name: str):
    conn = sqlite3.connect("app/data/recipes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM recipes WHERE LOWER(name) = LOWER(?)", (dish_name,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    # Assuming schema: id, name, cuisine, ingredients, instructions, cook_time, servings, region
    return {
        "name": row[1],
        "cuisine": row[2],
        "ingredients": row[3].split(","),
        "instructions": row[4],
        "cook_time": row[5],
        "servings": row[6],
        "region": row[7]
    }
