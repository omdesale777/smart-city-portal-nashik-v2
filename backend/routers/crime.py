"""
routers/crime.py — Crime Reporting Module endpoints

Endpoints:
    POST /api/crime-reports/          → Submit a crime/incident report
    GET  /api/crime-reports/          → List reports (admin only)
    GET  /api/crime-reports/{ref_id}  → Lookup by reference ID

Privacy guarantee:
    When is_anonymous=True, reporter_phone is stored as NULL.
    The ref_id is the ONLY link between the citizen and their report.
"""

import uuid
import json
import random
import string
from typing import List, Optional
from fastapi import APIRouter, File, Form, UploadFile, HTTPException, Query

from database import get_supabase, Tables
from models.schemas import CrimeReportCreate, CrimeReportResponse
from storage.upload_handler import upload_files

router = APIRouter()


def _generate_ref_id() -> str:
    """e.g. NKP-A3F9B2C1"""
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    return f"NKP-{suffix}"


# ── POST /api/crime-reports/ ─────────────────────────────────────
@router.post("/", response_model=CrimeReportResponse, status_code=201)
async def submit_crime_report(
    data:   str              = Form(...,  description="JSON string of CrimeReportCreate fields"),
    photos: List[UploadFile] = File(None, description="Up to 5 photos"),
    videos: List[UploadFile] = File(None, description="Up to 2 videos"),
):
    """
    Submit a crime/incident report with optional media evidence.

    When `is_anonymous` is true in the payload, no contact details
    are stored and the reporter_phone field is set to NULL.

    Example curl:
        curl -X POST http://localhost:8000/api/crime-reports/ \\
          -F 'data={"incident_type":"theft","urgency":"high",
                    "title":"Phone snatching near CBS","description":"Two men on black Pulsar",
                    "address":"CBS Road, Nashik","is_anonymous":true}' \\
          -F 'photos=@/path/to/evidence.jpg'
    """
    try:
        payload = CrimeReportCreate(**json.loads(data))
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

    # Upload media
    media_urls: List[str] = []
    if photos:
        valid = [f for f in photos if f.filename]
        if valid:
            media_urls += await upload_files(valid, folder="crime/photos")
    if videos:
        valid = [f for f in videos if f.filename]
        if valid:
            media_urls += await upload_files(valid, folder="crime/videos", compress_images=False)

    ref_id = _generate_ref_id()

    row = {
        "id":             str(uuid.uuid4()),
        "incident_type":  payload.incident_type,
        "urgency":        payload.urgency,
        "title":          payload.title,
        "description":    payload.description,
        "address":        payload.address,
        "ward":           payload.ward,
        "gps_lat":        payload.gps.lat if payload.gps else None,
        "gps_lng":        payload.gps.lng if payload.gps else None,
        "incident_time":  payload.incident_time.isoformat() if payload.incident_time else None,
        "suspect_count":  payload.suspect_count,
        "suspect_desc":   payload.suspect_desc,
        "is_anonymous":   payload.is_anonymous,
        # Enforce anonymity: never store phone if anonymous flag is set
        "reporter_phone": None if payload.is_anonymous else payload.reporter_phone,
        "media":          media_urls,
        "ref_id":         ref_id,
        "status":         "received",
    }

    sb = get_supabase()
    result = sb.table(Tables.CRIME_REPORTS).insert(row).execute()

    if not result.data:
        raise HTTPException(status_code=500, detail="Failed to save report to database.")

    return CrimeReportResponse(
        id=row["id"],
        ref_id=ref_id,
        status="received",
    )


# ── GET /api/crime-reports/ (admin) ─────────────────────────────
@router.get("/")
def list_crime_reports(
    urgency:       Optional[str] = Query(None),
    incident_type: Optional[str] = Query(None),
    status:        Optional[str] = Query(None),
    limit:         int            = Query(50, ge=1, le=200),
    offset:        int            = Query(0, ge=0),
):
    """
    List crime reports for police/admin dashboard.
    IMPORTANT: Add proper authentication before deploying publicly.
    Reporter phone is excluded from this response for privacy.
    """
    sb = get_supabase()
    query = sb.table(Tables.CRIME_REPORTS).select(
        "id, ref_id, incident_type, urgency, title, address, ward, status, created_at, is_anonymous"
    ).order("created_at", desc=True).limit(limit).offset(offset)

    if urgency:
        query = query.eq("urgency", urgency)
    if incident_type:
        query = query.eq("incident_type", incident_type)
    if status:
        query = query.eq("status", status)

    result = query.execute()
    return result.data or []


# ── GET /api/crime-reports/{ref_id} ─────────────────────────────
@router.get("/{ref_id}")
def get_crime_report(ref_id: str):
    """
    Fetch a report by its reference ID (e.g. NKP-A3F9B2C1).
    Returns only non-sensitive fields.
    """
    sb = get_supabase()
    result = sb.table(Tables.CRIME_REPORTS)\
        .select("id, ref_id, incident_type, urgency, title, address, ward, status, created_at")\
        .eq("ref_id", ref_id.upper())\
        .single()\
        .execute()

    if not result.data:
        raise HTTPException(status_code=404, detail=f"Report '{ref_id}' not found.")

    return result.data
