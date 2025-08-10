# app/utils/formatter.py
def format_recipe_response(data):
    return (
        f"🍽 Dish: {data['name']}\n"
        f"🕒 Cooking Time: {data['cook_time']} mins | Serves: {data['servings']}\n"
        f"📍 Famous in: {data['region']}\n\n"
        f"🛒 Ingredients:\n" + "\n".join([f"- {i}" for i in data['ingredients']]) + "\n\n"
        f"👨‍🍳 Steps:\n{data['instructions']}"
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


