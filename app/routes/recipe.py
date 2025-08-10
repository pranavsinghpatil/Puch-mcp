from fastapi import APIRouter, Query
from app.services.recipe_service import get_recipe_details
from app.utils.formatter import (
    format_recipe_response,
    format_options_response,
    format_guess_with_options
)
from time import time
import re

# ===== NLP Imports =====
import spacy
from rapidfuzz import fuzz, process

nlp = spacy.load("en_core_web_sm")

# Basic food synonyms dictionary
SYNONYMS = {
    "aubergine": "eggplant",
    "brinjal": "eggplant",
    "baingan": "eggplant",
    "paneer": "cottage cheese",
    "chole": "chickpeas",
    "rajma": "kidney beans"
}

# Intent keywords
DIET_KEYWORDS = ["vegetarian", "vegan", "gluten-free", "non-veg", "non vegetarian"]
COURSE_KEYWORDS = ["breakfast", "lunch", "dinner", "snack", "dessert", "main course", "side dish"]

router = APIRouter()

# In-memory user session store
active_user_sessions = {}
SESSION_TIMEOUT = 180  # seconds

def set_user_session(user_id: str, data: dict):
    active_user_sessions[user_id] = {
        **data,
        "timestamp": time()
    }

def get_user_session(user_id: str):
    session = active_user_sessions.get(user_id)
    if not session:
        return None
    if time() - session["timestamp"] > SESSION_TIMEOUT:
        del active_user_sessions[user_id]
        return None
    return session

def clear_user_session(user_id: str):
    active_user_sessions.pop(user_id, None)

# ===== NLP Entity Extraction =====
def extract_entities(user_input: str):
    doc = nlp(user_input.lower())

    dish = None
    diet = None
    course = None

    # Replace synonyms
    for word, repl in SYNONYMS.items():
        user_input = re.sub(rf"\b{word}\b", repl, user_input, flags=re.IGNORECASE)

    # Detect diet and course
    for token in doc:
        if token.text in DIET_KEYWORDS:
            diet = token.text
        if token.text in COURSE_KEYWORDS:
            course = token.text

    # Guess dish name (noun chunks)
    noun_chunks = [chunk.text for chunk in doc.noun_chunks]
    if noun_chunks:
        dish = noun_chunks[0]  # First noun phrase as primary dish guess

    return dish, diet, course

# ===== Route =====
@router.get("/get_recipe")
def get_recipe(user_id: str = Query(...), dish: str = Query(...)):
    dish_clean = dish.strip()

    # If user sends only a number
    if dish_clean.isdigit():
        session = get_user_session(user_id)
        if session and "options" in session:
            choice_idx = int(dish_clean) - 1
            if 0 <= choice_idx < len(session["options"]):
                chosen_dish = session["options"][choice_idx]
                clear_user_session(user_id)
                result = get_recipe_details(chosen_dish)
                if result and result["type"] == "recipe":
                    return {"response": format_recipe_response(result["data"])}
                else:
                    return {"response": f"❌ Sorry, I couldn't fetch details for '{chosen_dish}'."}
            else:
                return {"response": f"⚠ Invalid choice. Please reply dish name or a number between 1 and {len(session['options'])}."}
        return {"response": "⚠ No active choices found. Please type the dish name again."}

    # Extract NLP entities
    dish_entity, diet, course = extract_entities(dish_clean)

    # If no dish found, check if it’s a modification to last search
    if not dish_entity:
        session = get_user_session(user_id)
        if session and "last_dish" in session:
            dish_entity = session["last_dish"]
            # Override stored diet/course if mentioned
            diet = diet or session.get("diet")
            course = course or session.get("course")

    # Run search
    result = get_recipe_details(dish_entity)

    # Store context for future messages
    set_user_session(user_id, {
        "last_dish": dish_entity,
        "diet": diet,
        "course": course,
        "options": result["options"] if result and "options" in result else []
    })

    # Response handling
    if not result:
        return {"response": f"❌ Sorry, I couldn't find anything for '{dish_entity}'."}

    if result["type"] == "recipe":
        return {"response": format_recipe_response(result["data"])}

    if result["type"] == "guess_with_options":
        return {"response": format_guess_with_options(result["guess"], result["options"])}

    if result["type"] == "options":
        return {"response": format_options_response(result["data"])}

    return {"response": "⚠ Unexpected error occurred."}
