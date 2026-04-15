"""
routers/admin.py — Admin authentication and protected data endpoints

Endpoints:
    POST  /api/admin/login                  → Returns JWT token
    GET   /api/admin/me                     → Returns current admin info
    GET   /api/admin/grievances             → NMC only — list all grievances
    PATCH /api/admin/grievances/{id}        → NMC only — update status
    GET   /api/admin/crime-reports          → Police only — list all crime reports
    PATCH /api/admin/crime-reports/{id}     → Police only — update status
    GET   /api/admin/stats                  → Role-scoped stats for dashboard
"""

import os
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from database import get_supabase, Tables

router  = APIRouter()
bearer  = HTTPBearer()
pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ── Config ────────────────────────────────────────────────────────
JWT_SECRET    = os.environ.get("APP_SECRET", "change-me-in-production-32chars!!")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_HOURS = 8


# ══════════════════════════════════════════════════════════════════
#  SCHEMAS
# ══════════════════════════════════════════════════════════════════

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type:   str = "bearer"
    role:         str
    username:     str
    expires_in:   int  # seconds

class StatusUpdate(BaseModel):
    status: str   # submitted | in_progress | resolved | rejected


# ══════════════════════════════════════════════════════════════════
#  JWT HELPERS
# ══════════════════════════════════════════════════════════════════

def _create_token(username: str, role: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(hours=JWT_EXPIRE_HOURS)
    return jwt.encode(
        {"sub": username, "role": role, "exp": expire},
        JWT_SECRET,
        algorithm=JWT_ALGORITHM,
    )


def _decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token. Please log in again.",
            headers={"WWW-Authenticate": "Bearer"},
        )


# ── Dependency: any authenticated admin ──────────────────────────
def get_current_admin(
    creds: HTTPAuthorizationCredentials = Depends(bearer),
) -> dict:
    return _decode_token(creds.credentials)


# ── Dependency: NMC admin only ───────────────────────────────────
def require_nmc(admin: dict = Depends(get_current_admin)) -> dict:
    if admin.get("role") != "nmc":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. This endpoint requires NMC admin role.",
        )
    return admin


# ── Dependency: Police admin only ───────────────────────────────
def require_police(admin: dict = Depends(get_current_admin)) -> dict:
    if admin.get("role") != "police":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. This endpoint requires Police admin role.",
        )
    return admin


# ══════════════════════════════════════════════════════════════════
#  AUTH ENDPOINTS
# ══════════════════════════════════════════════════════════════════

@router.post("/login", response_model=LoginResponse)
def login(body: LoginRequest):
    """
    Validate admin credentials and return a JWT token.
    Passwords are verified against bcrypt hashes stored in Supabase.
    """
    sb = get_supabase()
    result = sb.table("admins") \
        .select("id, username, password_hash, role") \
        .eq("username", body.username.strip()) \
        .single() \
        .execute()

    admin = result.data
    if not admin or not pwd_ctx.verify(body.password, admin["password_hash"]):
        # Same error message for wrong username OR wrong password (security)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password.",
        )

    token = _create_token(admin["username"], admin["role"])
    return LoginResponse(
        access_token=token,
        role=admin["role"],
        username=admin["username"],
        expires_in=JWT_EXPIRE_HOURS * 3600,
    )


@router.get("/me")
def get_me(admin: dict = Depends(get_current_admin)):
    """Returns the currently authenticated admin's info."""
    return {"username": admin["sub"], "role": admin["role"]}


# ══════════════════════════════════════════════════════════════════
#  NMC — GRIEVANCES
# ══════════════════════════════════════════════════════════════════

VALID_GRIEVANCE_STATUSES = {"submitted", "in_progress", "resolved", "rejected"}

@router.get("/grievances")
def admin_list_grievances(
    status_filter: Optional[str] = None,
    issue_type:    Optional[str] = None,
    limit:         int = 100,
    offset:        int = 0,
    admin: dict = Depends(require_nmc),
):
    """
    NMC Admin: List all citizen grievances with full details.
    Supports filtering by status and issue_type.
    """
    sb = get_supabase()
    query = sb.table(Tables.GRIEVANCES) \
        .select(
            "id, ticket_id, issue_type, severity, title, description, "
            "address, ward, gps_lat, gps_lng, reporter_name, reporter_phone, "
            "reporter_email, photos, status, created_at"
        ) \
        .order("created_at", desc=True) \
        .limit(limit) \
        .offset(offset)

    if status_filter:
        query = query.eq("status", status_filter)
    if issue_type:
        query = query.eq("issue_type", issue_type)

    result = query.execute()
    return {
        "data":  result.data or [],
        "count": len(result.data or []),
        "admin": admin["sub"],
    }


@router.patch("/grievances/{grievance_id}")
def admin_update_grievance(
    grievance_id: str,
    body:  StatusUpdate,
    admin: dict = Depends(require_nmc),
):
    """NMC Admin: Update the status of a grievance."""
    if body.status not in VALID_GRIEVANCE_STATUSES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status. Must be one of: {VALID_GRIEVANCE_STATUSES}",
        )
    sb = get_supabase()
    result = sb.table(Tables.GRIEVANCES) \
        .update({"status": body.status}) \
        .eq("id", grievance_id) \
        .execute()

    if not result.data:
        raise HTTPException(status_code=404, detail="Grievance not found.")

    return {"success": True, "id": grievance_id, "new_status": body.status}


# ══════════════════════════════════════════════════════════════════
#  POLICE — CRIME REPORTS
# ══════════════════════════════════════════════════════════════════

VALID_CRIME_STATUSES = {"received", "under_review", "investigating", "closed", "rejected"}

@router.get("/crime-reports")
def admin_list_crime_reports(
    status_filter:  Optional[str] = None,
    incident_type:  Optional[str] = None,
    urgency:        Optional[str] = None,
    limit:          int = 100,
    offset:         int = 0,
    admin: dict = Depends(require_police),
):
    """
    Police Admin: List all crime reports.
    Reporter phone is included ONLY when is_anonymous=False.
    """
    sb = get_supabase()
    query = sb.table(Tables.CRIME_REPORTS) \
        .select(
            "id, ref_id, incident_type, urgency, title, description, "
            "address, ward, gps_lat, gps_lng, incident_time, "
            "suspect_count, suspect_desc, is_anonymous, reporter_phone, "
            "media, status, created_at"
        ) \
        .order("created_at", desc=True) \
        .limit(limit) \
        .offset(offset)

    if status_filter:
        query = query.eq("status", status_filter)
    if incident_type:
        query = query.eq("incident_type", incident_type)
    if urgency:
        query = query.eq("urgency", urgency)

    result = query.execute()

    # Enforce anonymity — blank out phone for anonymous reports
    data = result.data or []
    for row in data:
        if row.get("is_anonymous"):
            row["reporter_phone"] = None

    return {
        "data":  data,
        "count": len(data),
        "admin": admin["sub"],
    }


@router.patch("/crime-reports/{report_id}")
def admin_update_crime_report(
    report_id: str,
    body:  StatusUpdate,
    admin: dict = Depends(require_police),
):
    """Police Admin: Update the status of a crime report."""
    if body.status not in VALID_CRIME_STATUSES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status. Must be one of: {VALID_CRIME_STATUSES}",
        )
    sb = get_supabase()
    result = sb.table(Tables.CRIME_REPORTS) \
        .update({"status": body.status}) \
        .eq("id", report_id) \
        .execute()

    if not result.data:
        raise HTTPException(status_code=404, detail="Crime report not found.")

    return {"success": True, "id": report_id, "new_status": body.status}


# ══════════════════════════════════════════════════════════════════
#  STATS (role-scoped)
# ══════════════════════════════════════════════════════════════════

@router.get("/stats")
def admin_stats(admin: dict = Depends(get_current_admin)):
    """
    Returns dashboard stats scoped to the admin's role.
    NMC sees grievance stats. Police sees crime report stats.
    """
    sb   = get_supabase()
    role = admin["role"]

    if role == "nmc":
        rows = sb.table(Tables.GRIEVANCES).select("status, issue_type").execute().data or []
        total = len(rows)
        by_status = {}
        by_type   = {}
        for r in rows:
            s = r.get("status", "unknown")
            t = r.get("issue_type", "unknown")
            by_status[s] = by_status.get(s, 0) + 1
            by_type[t]   = by_type.get(t, 0) + 1
        return {
            "role": "nmc",
            "total": total,
            "by_status": by_status,
            "by_type":   by_type,
        }

    elif role == "police":
        rows = sb.table(Tables.CRIME_REPORTS).select("status, incident_type, urgency").execute().data or []
        total  = len(rows)
        by_status   = {}
        by_type     = {}
        by_urgency  = {}
        for r in rows:
            s = r.get("status",        "unknown")
            t = r.get("incident_type", "unknown")
            u = r.get("urgency",       "unknown")
            by_status[s]  = by_status.get(s, 0)  + 1
            by_type[t]    = by_type.get(t, 0)    + 1
            by_urgency[u] = by_urgency.get(u, 0) + 1
        return {
            "role": "police",
            "total":       total,
            "by_status":   by_status,
            "by_type":     by_type,
            "by_urgency":  by_urgency,
        }

    raise HTTPException(status_code=400, detail="Unknown role.")