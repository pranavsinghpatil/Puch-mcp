from fastapi import APIRouter, Query
from app.services.recipe_service import (
    get_recipe_details,
    get_recommendations,
    get_full_recipes_from_names
)
from app.utils.formatter import (
    format_recipe_response,
    format_options_response,
    format_guess_with_options
)
from time import time
import re
import spacy

# Load NLP model once
nlp = spacy.load("en_core_web_sm")

# Synonyms map for better matching
SYNONYMS = {
    "aubergine": "eggplant",
    "brinjal": "eggplant",
    "baingan": "eggplant",
    "paneer": "cottage cheese",
    "chole": "chickpeas",
    "rajma": "kidney beans"
}

# Keywords for special filtering
DIET_KEYWORDS = ["vegetarian", "vegan", "gluten-free", "non-veg", "non vegetarian"]
COURSE_KEYWORDS = ["breakfast", "lunch", "dinner", "snack", "dessert", "main course", "side dish"]

router = APIRouter()

# Session store
active_user_sessions = {}
SESSION_TIMEOUT = 180  # seconds

# ------------------ SESSION HELPERS ------------------ #
def set_user_session(user_id: str, data: dict):
    active_user_sessions[user_id] = {**data, "timestamp": time()}

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

# ------------------ NLP HELPERS ------------------ #
def extract_entities(user_input: str):
    # Replace synonyms before processing
    for word, repl in SYNONYMS.items():
        user_input = re.sub(rf"\b{word}\b", repl, user_input, flags=re.IGNORECASE)

    doc = nlp(user_input.lower())

    dish = None
    diet = None
    course = None

    for token in doc:
        if token.text in DIET_KEYWORDS:
            diet = token.text
        if token.text in COURSE_KEYWORDS:
            course = token.text

    noun_chunks = [chunk.text for chunk in doc.noun_chunks]
    if noun_chunks:
        dish = noun_chunks[0]

    return dish, diet, course

# ------------------ MAIN ROUTE ------------------ #
@router.get("/get_recipe")
def get_recipe(user_id: str = Query(...), dish: str = Query(...)):
    dish_clean = dish.strip().lower()

    # -------- Handle numeric choice -------- #
    if dish_clean.isdigit():
        session = get_user_session(user_id)
        if not session:
            return {"response": "⚠ No list to choose from right now. Try searching again."}

        choice_idx = int(dish_clean) - 1

        # Prefer explicit options (returned from fuzzy search)
        options = session.get("options") or []
        source = "options"
        if not options:
            # Fallback to recommendations list if options absent
            options = session.get("recommendations") or []
            source = "recommendations"
        if not options:
            return {"response": "⚠ No list to choose from right now. Try searching again."}

        if 0 <= choice_idx < len(options):
            chosen_dish = options[choice_idx]
            clear_user_session(user_id)
            result = get_recipe_details(chosen_dish)

            if result and result.get("type") == "recipe":
                return {"response": format_recipe_response(result["data"])}
            else:
                return {"response": f"❌ Sorry, I couldn't fetch details for '{chosen_dish}'."}
        else:
            return {"response": f"⚠ Invalid choice. Please reply with a number between 1 and {len(options)}."}

    # -------- Handle "show more" request -------- #
    if dish_clean in ["show more", "showmore", "more"]:
        session = get_user_session(user_id)
        if not session or "recommendations" not in session or not session["recommendations"]:
            return {"response": "⚠ No saved recommendations. Please search for a dish first."}

        full_recipes = get_full_recipes_from_names(session["recommendations"])
        clear_user_session(user_id)

        if not full_recipes:
            return {"response": "❌ Sorry, no recipes found for those recommendations."}

        return {"response": "\n\n".join(format_recipe_response(r) for r in full_recipes)}

    # -------- Substring match against previous suggestions -------- #
    session = get_user_session(user_id)
    if session:
        candidates = (session.get("options") or []) + (session.get("recommendations") or [])
        for name in candidates:
            if dish_clean in name.lower():
                # treat this as user selecting that dish
                clear_user_session(user_id)
                result = get_recipe_details(name)
                if result and result.get("type") == "recipe":
                    return {"response": format_recipe_response(result["data"])}
                break

    # -------- Extract search entities -------- #
    dish_entity, diet, course = extract_entities(dish_clean)

    # Fallback to last search if dish not found
    if not dish_entity:
        session = get_user_session(user_id)
        if session:
            dish_entity = session.get("last_dish", dish_clean)
            diet = diet or session.get("diet")
            course = course or session.get("course")
        else:
            dish_entity = dish_clean

    # -------- Fetch main recipe -------- #
    result = get_recipe_details(dish_entity, diet=diet, course=course)

    if not result:
        return {"response": f"❌ Sorry, I couldn't find anything for '{dish_entity}'."}

    # -------- Get recommendations -------- #
    recs = get_recommendations(dish_entity, diet=diet, course=course, top_n=3)
    rec_names = [r[0] for r in recs]
    rec_courses = [r[1] for r in recs]

    # Store session for later
    set_user_session(user_id, {
        "last_dish": dish_entity,
        "diet": diet,
        "course": course,
        "options": result.get("options", []),
        "recommendations": rec_names
    })

    # -------- Build main response -------- #
    if result["type"] == "recipe":
        base_resp = format_recipe_response(result["data"])
    elif result["type"] == "guess_with_options":
        base_resp = format_guess_with_options(result["guess"], result["options"])
    elif result["type"] == "options":
        base_resp = format_options_response(result["data"])
    else:
        base_resp = "⚠ Unexpected error occurred while fetching the recipe."

    # -------- Append recommendations preview -------- #
    if recs:
        rec_lines = [
            f"{i+1}. {name} ({course})" if course else f"{i+1}. {name}"
            for i, (name, course) in enumerate(recs)
        ]
        base_resp += (
            "\n\n💡 You might also like:\n" +
            "\n".join(rec_lines) +
            "\n(Reply with the name or number to see details!)"
        )

    return {"response": base_resp}
