import os
import pandas as pd
from rapidfuzz import fuzz, process

# Path to your cleaned CSV
DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/recipes.csv")

# Load once
df = pd.read_csv(DATA_PATH, dtype=str).fillna("")  # ensure strings
# Normalize columns used later
for col in ["name", "description", "cuisine", "course", "diet", "ingredients", "instructions", "image_url"]:
    if col not in df.columns:
        df[col] = ""

# Pre-compute a combined searchable text for each row
SEARCH_COLUMNS = ["name", "description", "cuisine", "course", "diet", "ingredients"]
df["search_text"] = df[SEARCH_COLUMNS].apply(lambda row: " ".join(row.values.astype(str)), axis=1)

# Helper: check if row matches diet/course filter (case-insensitive partial)
def matches_filter(value: str, filter_term: str) -> bool:
    if not filter_term:
        return True
    return filter_term.strip().lower() in value.strip().lower()

def _collect_matches(query: str, limit: int = 20, score_threshold: int = 50):
    """Return list of ``(score:int, idx:int)`` sorted by ``score`` desc.

    Improvements over the previous implementation:
    1. **Dual-field matching** – We now search on both the pre-computed *search_text* **and** the
       canonical *name* column.  Misspellings often retain phonetic similarity to the dish name
       but share *zero* token overlap with the full descriptive text (e.g. "biriani" vs
       "Chicken Biryani").  By separately matching against the shorter *name* field with a more
       permissive scorer we capture these cases.
    2. **WRatio scorer** – For name matching we leverage ``rapidfuzz.fuzz.WRatio`` which is a
       composite scorer combining multiple fuzzy algorithms (ratio, partial ratio, token sort,
       etc.) giving robust results for typos and reordered tokens.
    3. **Score aggregation** – When the same row appears in both result sets we keep the highest
       score. Finally we filter by ``score_threshold`` and return the top ``limit`` matches.
    """
    # --- Match against the long combined field (good for descriptive queries) ---
    raw_search = process.extract(
        query,
        df["search_text"].tolist(),
        scorer=fuzz.token_set_ratio,
        limit=limit * 2  # grab more to merge later
    )

    # --- Match against the recipe *name* directly (good for typos / short queries) ---
    raw_name = process.extract(
        query,
        df["name"].tolist(),
        scorer=fuzz.WRatio,
        limit=limit * 2
    )

    # Combine keeping the highest score per dataframe index
    combined: dict[int, int] = {}
    for (_, score, idx) in raw_search + raw_name:
        sc = int(score)
        if sc >= score_threshold:
            if idx not in combined or sc > combined[idx]:
                combined[idx] = sc

    # Convert to list sorted by score desc
    matches = sorted([(s, i) for i, s in combined.items()], key=lambda x: x[0], reverse=True)[:limit]
    return matches

def get_recipe_details(query: str, diet: str = None, course: str = None, limit: int = 5):
    """
    Main search function.
    - query: user query string (dish or description)
    - diet: optional diet filter (e.g., "vegetarian")
    - course: optional course filter (e.g., "lunch")
    Returns:
        - {"type": "recipe", "data": {...}}
        - {"type": "guess_with_options", "guess": name, "options": [...]}
        - {"type": "options", "data": [...]}
        - None if nothing relevant found
    """
    if not query:
        return None

    # Collect fuzzy matches across combined text
    matches = _collect_matches(query, limit=40, score_threshold=40)  # wide net first
    if not matches:
        return None

    # Apply diet & course filtering if provided, but keep note if filter eliminates all -> fallback
    filtered = []
    for score, idx in matches:
        row = df.iloc[idx]
        if matches_filter(row.get("diet", ""), diet) and matches_filter(row.get("course", ""), course):
            filtered.append((score, idx, row))

    used_filtered = True
    if not filtered:
        # If filter removed everything, fall back to unfiltered matches (but mark used_filtered False)
        used_filtered = False
        filtered = [(s, i, df.iloc[i]) for s, i in matches]

    # Now decide response based on top scores
    filtered.sort(key=lambda x: x[0], reverse=True)
    top_score = filtered[0][0]
    top_row = filtered[0][2]

    # If extremely confident -> return recipe (lowered threshold for typos)
    if top_score >= 80:
        recipe = top_row.to_dict()
        return {"type": "recipe", "data": recipe}

    # If moderately confident -> give guess_with_options
    elif 60 <= top_score < 80:
        options = []
        seen = set()
        for score, idx, row in filtered:
            name = row["name"]
            if name not in seen:
                options.append(name)
                seen.add(name)
            if len(options) >= limit:
                break
        guess = top_row["name"]
        return {"type": "guess_with_options", "guess": guess, "options": options}

    # Else lower confidence -> show multiple relevant options as choices
    else:
        options = []
        seen = set()
        for score, idx, row in filtered[:limit]:
            name = row["name"]
            if name not in seen:
                options.append(name)
                seen.add(name)
        if options:
            return {"type": "options", "data": options}
        return None

def get_recommendations(keyword: str, diet: str = None, course: str = None, top_n: int = 5):
    """
    Returns top dish name + course tuples as recommendations.
    If no keyword, returns first N rows.
    """
    recs = []

    if not keyword:
        for _, row in df.head(top_n).iterrows():
            recs.append((row["name"], row.get("course", "")))
        return recs

    matches = _collect_matches(keyword, limit=200, score_threshold=30)
    if not matches:
        return []

    seen = set()
    for score, idx in matches:
        row = df.iloc[idx]
        if matches_filter(row.get("diet", ""), diet) and matches_filter(row.get("course", ""), course):
            if row["name"] not in seen:
                recs.append((row["name"], row.get("course", "")))
                seen.add(row["name"])
        if len(recs) >= top_n:
            break

    if not recs:
        # Relax filters if nothing found
        for score, idx in matches:
            row = df.iloc[idx]
            if row["name"] not in seen:
                recs.append((row["name"], row.get("course", "")))
                seen.add(row["name"])
            if len(recs) >= top_n:
                break

    return recs

def get_full_recipes_from_names(names: list):
    """
    Given a list of recipe names, return full recipe data from the dataframe.
    """
    results = []
    for name in names:
        row_match = df[df["name"].str.lower() == name.strip().lower()]
        if not row_match.empty:
            results.append(row_match.iloc[0].to_dict())
    return results
