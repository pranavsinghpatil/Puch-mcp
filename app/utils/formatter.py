# app/utils/formatter.py
def format_recipe_response(data):
    return (
        f"🍽 Dish: {data.get('name', 'N/A')}\n"
        f"📖 Description: {data.get('description', 'No description')}\n"
        f"🍲 Cuisine: {data.get('cuisine', 'Unknown')}\n"
        f"📚 Course: {data.get('course', 'Unknown')}\n"
        f"🥗 Diet: {data.get('diet', 'Unknown')}\n"
        f"⏱ Prep Time: {data.get('prep_time', 'Unknown')}\n"
        f"🛒 Ingredients: {data.get('ingredients', 'Not listed')}\n"
        f"📝 Instructions: {data.get('instructions', 'Not provided')}\n"
        # f"🖼 Image: {data.get('image_url', 'No image')}"
    )

def format_options_response(options):
    return "I found several matching dishes:\n" + "\n".join(
        [f"{i+1}. {opt}" for i, opt in enumerate(options)]
    ) + "\n\nPlease reply with the exact name or number."

def format_guess_with_options(guess, options):
    return (
        f"🤔 Did you mean '{guess}'?\nHere are similar dishes:\n"
        + "\n".join([f"{i+1}. {opt}" for i, opt in enumerate(options)])
        + "\n\nPlease reply with the name or number."
    )



def format_locality_response(dish, city, places):
    response = f"📍 Where to find *{dish}* in {city}:\n"
    for p in places:
        response += f"🍴 {p['name']} (⭐ {p['rating']})\n"
        response += f"📍 {p['address']}\n"
        response += f"🔗 [View on Maps]({p['maps_url']})\n\n"
    return response.strip()

def format_recommendation_response(dish, recs):
    response = f"🍽 If you like *{dish}*, you might also enjoy:\n"
    for r in recs:
        response += f"- {r}\n"
    return response.strip()


