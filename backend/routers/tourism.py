"""
routers/tourism.py — Nashik Bhatakanti: Travel Guide endpoints

Endpoints:
    GET /api/tourism/spots              → List all tourist spots (with optional filters)
    GET /api/tourism/spots/{id}         → Single tourist spot detail
    GET /api/tourism/categories         → List available categories with counts
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query

from database import get_supabase, Tables
from models.schemas import TouristSpotOut

router = APIRouter()


# ── List tourist spots ────────────────────────────────────────────

@router.get("/spots", response_model=List[TouristSpotOut])
def list_tourist_spots(
    category:     Optional[str] = Query(None, description="fort | waterfall | adventure | nature | history"),
    difficulty:   Optional[str] = Query(None, description="easy | moderate | hard"),
    max_distance: Optional[int] = Query(None, ge=1, description="Max distance from Nashik city in km"),
    search:       Optional[str] = Query(None, description="Search by name or description"),
):
    """
    Returns tourist spots from the Bhatakanti travel guide.
    Supports filtering by category, difficulty, max distance, and text search.
    """
    sb = get_supabase()
    query = sb.table(Tables.TOURIST_SPOTS)\
        .select("*")\
        .order("rating", desc=True)

    if category:
        query = query.eq("category", category.lower())
    if difficulty:
        query = query.eq("difficulty", difficulty.lower())
    if max_distance:
        query = query.lte("distance_km", max_distance)
    if search:
        # Supabase text search via ilike on name column
        query = query.ilike("name", f"%{search}%")

    result = query.execute()
    return result.data or []


# ── Single tourist spot ───────────────────────────────────────────

@router.get("/spots/{spot_id}", response_model=TouristSpotOut)
def get_tourist_spot(spot_id: str):
    """Fetch full details for a single tourist spot by ID."""
    sb = get_supabase()
    result = sb.table(Tables.TOURIST_SPOTS)\
        .select("*").eq("id", spot_id).single().execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Tourist spot not found.")
    return result.data


# ── Category list with counts ─────────────────────────────────────

@router.get("/categories")
def list_categories():
    """
    Returns the list of categories with the count of spots in each.
    Useful for building dynamic filter tabs on the frontend.
    """
    sb = get_supabase()
    # Fetch all and count in Python (Supabase free tier doesn't support GROUP BY via API)
    result = sb.table(Tables.TOURIST_SPOTS).select("category").execute()
    counts: dict = {}
    for row in result.data or []:
        cat = row.get("category", "other")
        counts[cat] = counts.get(cat, 0) + 1

    return {
        "categories": [
            {"name": cat, "count": count}
            for cat, count in sorted(counts.items())
        ],
        "total": sum(counts.values()),
    }
