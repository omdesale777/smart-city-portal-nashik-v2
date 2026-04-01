"""
routers/kumbhnagari.py — Kumbhnagari Nashik: Tourism + Hotels + Spiritual

Endpoints:
    GET /api/kumbhnagari/hotels              → List all hotels
    GET /api/kumbhnagari/hotels/{id}         → Single hotel
    GET /api/kumbhnagari/spiritual           → List spiritual spots
    GET /api/kumbhnagari/spiritual/{id}      → Single spiritual spot
    GET /api/kumbhnagari/events              → Upcoming spiritual events
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query

from database import get_supabase, Tables
from models.schemas import HotelOut, SpiritualSpotOut, SpiritualEventOut

router = APIRouter()


# ── Hotels ────────────────────────────────────────────────────────

@router.get("/hotels", response_model=List[HotelOut])
def list_hotels(
    min_stars: Optional[int] = Query(None, ge=1, le=5, description="Filter by minimum star rating"),
    area:      Optional[str] = Query(None, description="Filter by area name"),
):
    """
    Returns all hotels and lodges listed in the Kumbhnagari module.
    Optionally filter by star rating or area (e.g. 'Panchavati').
    """
    sb = get_supabase()
    query = sb.table(Tables.HOTELS)\
        .select("*")\
        .order("stars", desc=True)

    if min_stars:
        query = query.gte("stars", min_stars)
    if area:
        query = query.ilike("area", f"%{area}%")

    result = query.execute()
    return result.data or []


@router.get("/hotels/{hotel_id}", response_model=HotelOut)
def get_hotel(hotel_id: str):
    sb = get_supabase()
    result = sb.table(Tables.HOTELS)\
        .select("*").eq("id", hotel_id).single().execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Hotel not found.")
    return result.data


# ── Spiritual Spots ───────────────────────────────────────────────

@router.get("/spiritual", response_model=List[SpiritualSpotOut])
def list_spiritual_spots(
    category: Optional[str] = Query(None, description="Filter by category (temple, ghat, etc.)"),
):
    """
    Returns all spiritual spots — temples, ghats, holy sites.
    """
    sb = get_supabase()
    query = sb.table(Tables.SPIRITUAL)\
        .select("*")\
        .order("rating", desc=True)

    if category:
        query = query.ilike("category", f"%{category}%")

    result = query.execute()
    return result.data or []


@router.get("/spiritual/{spot_id}", response_model=SpiritualSpotOut)
def get_spiritual_spot(spot_id: str):
    sb = get_supabase()
    result = sb.table(Tables.SPIRITUAL)\
        .select("*").eq("id", spot_id).single().execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Spiritual spot not found.")
    return result.data


# ── Events ────────────────────────────────────────────────────────

@router.get("/events", response_model=List[SpiritualEventOut])
def list_events():
    """Returns all spiritual events and festivals."""
    sb = get_supabase()
    result = sb.table(Tables.EVENTS)\
        .select("*")\
        .order("created_at")\
        .execute()
    return result.data or []
