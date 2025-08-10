# app/routes/locality.py
from fastapi import APIRouter, Query
from ..services.locality_service import get_nearby_places
from ..utils.formatter import format_locality_response

router = APIRouter(prefix="/get_locality", tags=["Locality"])

@router.get("/")
def get_locality(dish: str = Query(...), city: str = Query(...)):
    places = get_nearby_places(dish, city)
    if not places:
        return {"error": "No nearby places found."}
    return {"response": format_locality_response(dish, city, places)}
