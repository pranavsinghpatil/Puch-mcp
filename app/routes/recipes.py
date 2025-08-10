# app/routes/recipe.py
from fastapi import APIRouter, Query
from services.recipe_service import get_recipe_details
from utils.formatter import format_recipe_response

router = APIRouter(prefix="/get_recipe", tags=["Recipe"])

@router.get("/")
def get_recipe(dish: str = Query(..., description="Dish name")):
    recipe_data = get_recipe_details(dish)
    if not recipe_data:
        return {"error": "Dish not found in our database."}
    return {"response": format_recipe_response(recipe_data)}
