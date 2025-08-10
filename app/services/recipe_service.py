import pandas as pd
from rapidfuzz import fuzz, process

df = pd.read_csv("app/data/recipes.csv")

SEARCH_COLUMNS = ["name", "description", "cuisine", "course", "diet", "ingredients"]

def search_all_columns(query):
    matches = []

    for idx, row in df.iterrows():
        combined_text = " ".join(str(row[col]) for col in SEARCH_COLUMNS if pd.notnull(row[col]))
        score = fuzz.partial_ratio(query.lower(), combined_text.lower())

        if score > 60:  # threshold for relevance
            matches.append((score, row))

    matches.sort(key=lambda x: x[0], reverse=True)
    return [row for score, row in matches]

def get_recipe_details(query):
    matches = search_all_columns(query)

    if not matches:
        return None

    # If only one match and score is high → return directly
    if len(matches) == 1:
        return {"type": "recipe", "data": matches[0].to_dict()}

    # If multiple matches → return top 5 with best guess
    top_matches = matches[:5]
    best_guess = top_matches[0]["name"]

    options = [m["name"] for m in top_matches]
    return {
        "type": "guess_with_options",
        "guess": best_guess,
        "options": options
    }

def get_recommendations(keyword):
    """Basic NLP recommendation system"""
    matches = search_all_columns(keyword)
    recs = [m["name"] for m in matches[:5]]
    return recs
