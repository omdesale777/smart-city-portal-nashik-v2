"""
routers/grievance.py — Citizen Grievance Portal endpoints

Endpoints:
    POST /api/grievances/         → Submit a new complaint (with optional photo upload)
    GET  /api/grievances/         → List all grievances (admin)
    GET  /api/grievances/{id}     → Get a single grievance by ID or ticket_id
"""

import uuid
import json
from typing import List, Optional
from fastapi import APIRouter, File, Form, UploadFile, HTTPException, Query

from database import get_supabase, Tables
from models.schemas import GrievanceCreate, GrievanceResponse, GrievanceListItem
from storage.upload_handler import upload_files

router = APIRouter()


def _generate_ticket_id() -> str:
    """e.g. NMC-384920"""
    import random
    return f"NMC-{random.randint(100000, 999999)}"


# ── POST /api/grievances/ ────────────────────────────────────────
@router.post("/", response_model=GrievanceResponse, status_code=201)
async def submit_grievance(
    data:   str              = Form(...,  description="JSON string of GrievanceCreate fields"),
    photos: List[UploadFile] = File(None, description="Up to 5 photos"),
):
    """
    Submit a new citizen grievance.

    The form body uses multipart so photos can be included.
    `data` is a JSON-encoded string of all text fields.

    Example curl:
        curl -X POST http://localhost:8000/api/grievances/ \\
          -F 'data={"issue_type":"road","severity":"high","title":"Pothole on CBS Road",
                    "description":"Large pothole near SBI ATM","address":"CBS Road, Nashik",
                    "reporter_phone":"9876543210"}' \\
          -F 'photos=@/path/to/photo.jpg'
    """
    # Parse and validate the JSON payload
    try:
        payload = GrievanceCreate(**json.loads(data))
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

    # Upload photos if provided
    photo_urls: List[str] = []
    if photos:
        valid_photos = [f for f in photos if f.filename]  # filter empty
        if valid_photos:
            photo_urls = await upload_files(valid_photos, folder="grievances")

    ticket_id = _generate_ticket_id()

    row = {
        "id":             str(uuid.uuid4()),
        "issue_type":     payload.issue_type,
        "severity":       payload.severity,
        "title":          payload.title,
        "description":    payload.description,
        "address":        payload.address,
        "ward":           payload.ward,
        "gps_lat":        payload.gps.lat if payload.gps else None,
        "gps_lng":        payload.gps.lng if payload.gps else None,
        "reporter_name":  payload.reporter_name,
        "reporter_phone": payload.reporter_phone,
        "reporter_email": payload.reporter_email,
        "photos":         photo_urls,
        "ticket_id":      ticket_id,
        "status":         "submitted",
    }

    sb = get_supabase()
    result = sb.table(Tables.GRIEVANCES).insert(row).execute()

    if not result.data:
        raise HTTPException(status_code=500, detail="Failed to save grievance to database.")

    return GrievanceResponse(
        id=row["id"],
        ticket_id=ticket_id,
        status="submitted",
    )


# ── GET /api/grievances/ ─────────────────────────────────────────
@router.get("/", response_model=List[GrievanceListItem])
def list_grievances(
    status:     Optional[str] = Query(None, description="Filter by status"),
    issue_type: Optional[str] = Query(None, description="Filter by issue_type"),
    limit:      int            = Query(50, ge=1, le=200),
    offset:     int            = Query(0, ge=0),
):
    """
    List all grievances (intended for admin/municipal dashboard).
    Add authentication middleware before exposing this publicly.
    """
    sb = get_supabase()
    query = sb.table(Tables.GRIEVANCES).select(
        "id, ticket_id, issue_type, title, severity, address, ward, status, created_at"
    ).order("created_at", desc=True).limit(limit).offset(offset)

    if status:
        query = query.eq("status", status)
    if issue_type:
        query = query.eq("issue_type", issue_type)

    result = query.execute()
    return result.data or []


# ── GET /api/grievances/{ticket_id} ──────────────────────────────
@router.get("/{ticket_id}", response_model=GrievanceListItem)
def get_grievance(ticket_id: str):
    """Fetch a single grievance by ticket_id (e.g. NMC-384920)."""
    sb = get_supabase()
    result = sb.table(Tables.GRIEVANCES)\
        .select("id, ticket_id, issue_type, title, severity, address, ward, status, created_at")\
        .eq("ticket_id", ticket_id.upper())\
        .single()\
        .execute()

    if not result.data:
        raise HTTPException(status_code=404, detail=f"Grievance '{ticket_id}' not found.")

    return result.data
