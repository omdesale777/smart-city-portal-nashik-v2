"""
models/schemas.py — Pydantic models for request/response validation

All four modules' schemas live here so imports stay clean:
    from models.schemas import GrievanceCreate, CrimeReportCreate, ...
"""

from __future__ import annotations
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, validator
import re


# ══════════════════════════════════════════════════════════════
#  SHARED
# ══════════════════════════════════════════════════════════════

class GPSCoords(BaseModel):
    lat: float = Field(..., ge=-90,  le=90)
    lng: float = Field(..., ge=-180, le=180)


class SuccessResponse(BaseModel):
    success: bool = True
    message: str


# ══════════════════════════════════════════════════════════════
#  CITIZEN GRIEVANCE PORTAL
# ══════════════════════════════════════════════════════════════

GRIEVANCE_ISSUE_TYPES = {
    "garbage", "road", "streetlight", "tree", "water", "other"
}
GRIEVANCE_SEVERITIES = {"low", "medium", "high"}


class GrievanceCreate(BaseModel):
    issue_type:      str = Field(..., description="One of: garbage | road | streetlight | tree | water | other")
    severity:        str = Field("medium", description="low | medium | high")
    title:           str = Field(..., min_length=5, max_length=120)
    description:     str = Field(..., min_length=10, max_length=500)
    address:         str = Field(..., min_length=5, max_length=250)
    ward:            Optional[str] = None
    gps:             Optional[GPSCoords] = None
    reporter_name:   Optional[str] = Field(None, max_length=100)
    reporter_phone:  str = Field(..., description="10-digit mobile number")
    reporter_email:  Optional[str] = Field(None, max_length=120)
    photos_count:    int = Field(0, ge=0, le=5)

    @validator("issue_type")
    def validate_issue_type(cls, v):
        if v not in GRIEVANCE_ISSUE_TYPES:
            raise ValueError(f"issue_type must be one of {GRIEVANCE_ISSUE_TYPES}")
        return v

    @validator("severity")
    def validate_severity(cls, v):
        if v not in GRIEVANCE_SEVERITIES:
            raise ValueError(f"severity must be one of {GRIEVANCE_SEVERITIES}")
        return v

    @validator("reporter_phone")
    def validate_phone(cls, v):
        if not re.fullmatch(r"\d{10}", v):
            raise ValueError("reporter_phone must be exactly 10 digits")
        return v


class GrievanceResponse(BaseModel):
    id:        str
    ticket_id: str
    status:    str
    message:   str = "Complaint submitted successfully"


class GrievanceListItem(BaseModel):
    id:         str
    ticket_id:  str
    issue_type: str
    title:      str
    severity:   str
    address:    str
    ward:       Optional[str]
    status:     str
    created_at: datetime


# ══════════════════════════════════════════════════════════════
#  CRIME REPORTING
# ══════════════════════════════════════════════════════════════

INCIDENT_TYPES = {
    "theft", "harassment", "drugs", "assault", "suspicious", "other"
}
URGENCY_LEVELS = {"low", "medium", "high"}


class CrimeReportCreate(BaseModel):
    incident_type:   str = Field(..., description="theft | harassment | drugs | assault | suspicious | other")
    urgency:         str = Field("medium")
    title:           str = Field(..., min_length=5, max_length=120)
    description:     str = Field(..., min_length=10, max_length=800)
    address:         str = Field(..., min_length=5, max_length=250)
    ward:            Optional[str] = None
    gps:             Optional[GPSCoords] = None
    incident_time:   Optional[datetime] = None
    suspect_count:   Optional[str] = None
    suspect_desc:    Optional[str] = Field(None, max_length=300)
    is_anonymous:    bool = True
    reporter_phone:  Optional[str] = None   # required only when not anonymous
    photos_count:    int = Field(0, ge=0, le=5)
    videos_count:    int = Field(0, ge=0, le=2)

    @validator("incident_type")
    def validate_incident_type(cls, v):
        if v not in INCIDENT_TYPES:
            raise ValueError(f"incident_type must be one of {INCIDENT_TYPES}")
        return v

    @validator("urgency")
    def validate_urgency(cls, v):
        if v not in URGENCY_LEVELS:
            raise ValueError(f"urgency must be one of {URGENCY_LEVELS}")
        return v

    @validator("reporter_phone")
    def validate_phone(cls, v, values):
        if not values.get("is_anonymous") and v:
            if not re.fullmatch(r"\d{10}", v):
                raise ValueError("reporter_phone must be exactly 10 digits")
        return v


class CrimeReportResponse(BaseModel):
    id:     str
    ref_id: str
    status: str
    message: str = "Report submitted. Your identity is protected."


# ══════════════════════════════════════════════════════════════
#  KUMBHNAGARI — Hotels & Spiritual Spots
# ══════════════════════════════════════════════════════════════

class HotelOut(BaseModel):
    id:          str
    name:        str
    area:        Optional[str]
    stars:       Optional[int]
    price_from:  Optional[int]
    phone:       Optional[str]
    tags:        Optional[List[str]]
    website:     Optional[str]


class SpiritualSpotOut(BaseModel):
    id:          str
    name:        str
    name_deva:   Optional[str]
    category:    Optional[str]
    description: Optional[str]
    address:     Optional[str]
    gps_lat:     Optional[float]
    gps_lng:     Optional[float]
    timings:     Optional[str]
    entry_fee:   Optional[str]
    image_url:   Optional[str]
    rating:      Optional[float]


class SpiritualEventOut(BaseModel):
    id:          str
    name:        str
    icon:        Optional[str]
    when_text:   Optional[str]
    description: Optional[str]


# ══════════════════════════════════════════════════════════════
#  BHATAKANTI — Tourist Spots
# ══════════════════════════════════════════════════════════════

TOURIST_CATEGORIES = {"fort", "waterfall", "adventure", "nature", "history"}


class TouristSpotOut(BaseModel):
    id:           str
    name:         str
    category:     str
    description:  Optional[str]
    address:      Optional[str]
    distance_km:  Optional[int]
    difficulty:   Optional[str]
    entry_fee:    Optional[str]
    timings:      Optional[str]
    image_url:    Optional[str]
    map_link:     Optional[str]
    youtube_link: Optional[str]
    rating:       Optional[float]


class TouristSpotFilter(BaseModel):
    category:    Optional[str] = None
    max_distance: Optional[int] = None
    difficulty:  Optional[str] = None
