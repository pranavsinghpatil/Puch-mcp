# app/routes/recommend.py
from fastapi import APIRouter, Query
from services.recommend_service import recommend_dishes
from utils.formatter import format_recommendation_response

router = APIRouter(prefix="/recommend", tags=["Recommendation"])

@router.get("/")
def get_recommendations(dish: str = Query(...)):
    recs = recommend_dishes(dish)
    if not recs:
        return {"error": "No recommendations found."}
    return {"response": format_recommendation_response(dish, recs)}
