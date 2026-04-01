"""
database.py — Supabase client initialisation

Usage in any router:
    from database import get_supabase
    sb = get_supabase()
    result = sb.table("grievances").select("*").execute()
"""

import os
from functools import lru_cache
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()


@lru_cache(maxsize=1)
def get_supabase() -> Client:
    """
    Returns a cached Supabase client.
    Uses the service-role key so the backend can bypass Row Level Security
    for writes. Never expose this key to the frontend.
    """
    url  = os.environ.get("SUPABASE_URL")
    key  = os.environ.get("SUPABASE_SERVICE_KEY")

    if not url or not key:
        raise RuntimeError(
            "Missing SUPABASE_URL or SUPABASE_SERVICE_KEY in environment. "
            "Check your .env file."
        )

    return create_client(url, key)


def get_bucket() -> str:
    """Returns the Supabase Storage bucket name from env."""
    return os.environ.get("SUPABASE_BUCKET", "uploads")


# ── Supabase Table Names (single source of truth) ──────────────
class Tables:
    GRIEVANCES    = "grievances"
    CRIME_REPORTS = "crime_reports"
    HOTELS        = "hotels"
    SPIRITUAL     = "spiritual_spots"
    TOURIST_SPOTS = "tourist_spots"
    EVENTS        = "spiritual_events"


# ── SQL: Create tables (run once in Supabase SQL editor) ────────
"""
Copy-paste each block into Supabase → SQL Editor → Run

-- 1. Grievances
CREATE TABLE grievances (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    issue_type      TEXT NOT NULL,
    severity        TEXT NOT NULL DEFAULT 'medium',
    title           TEXT NOT NULL,
    description     TEXT NOT NULL,
    address         TEXT NOT NULL,
    ward            TEXT,
    gps_lat         NUMERIC,
    gps_lng         NUMERIC,
    reporter_name   TEXT,
    reporter_phone  TEXT,
    reporter_email  TEXT,
    photos          TEXT[],          -- array of Supabase Storage URLs
    status          TEXT NOT NULL DEFAULT 'submitted',
    ticket_id       TEXT UNIQUE,
    created_at      TIMESTAMPTZ DEFAULT now()
);

-- 2. Crime Reports
CREATE TABLE crime_reports (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    incident_type    TEXT NOT NULL,
    urgency          TEXT NOT NULL DEFAULT 'medium',
    title            TEXT NOT NULL,
    description      TEXT NOT NULL,
    address          TEXT NOT NULL,
    ward             TEXT,
    gps_lat          NUMERIC,
    gps_lng          NUMERIC,
    incident_time    TIMESTAMPTZ,
    suspect_count    TEXT,
    suspect_desc     TEXT,
    is_anonymous     BOOLEAN NOT NULL DEFAULT TRUE,
    reporter_phone   TEXT,           -- null if anonymous
    media            TEXT[],         -- Supabase Storage URLs
    ref_id           TEXT UNIQUE,
    status           TEXT NOT NULL DEFAULT 'received',
    created_at       TIMESTAMPTZ DEFAULT now()
);

-- 3. Hotels
CREATE TABLE hotels (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name        TEXT NOT NULL,
    area        TEXT,
    stars       INT CHECK (stars BETWEEN 1 AND 5),
    price_from  INT,                 -- INR per night
    phone       TEXT,
    tags        TEXT[],
    website     TEXT,
    created_at  TIMESTAMPTZ DEFAULT now()
);

-- 4. Spiritual Spots
CREATE TABLE spiritual_spots (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name        TEXT NOT NULL,
    name_deva   TEXT,
    category    TEXT,
    description TEXT,
    address     TEXT,
    gps_lat     NUMERIC,
    gps_lng     NUMERIC,
    timings     TEXT,
    entry_fee   TEXT,
    image_url   TEXT,
    rating      NUMERIC,
    created_at  TIMESTAMPTZ DEFAULT now()
);

-- 5. Tourist Spots (Bhatakanti)
CREATE TABLE tourist_spots (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name         TEXT NOT NULL,
    category     TEXT NOT NULL,    -- fort | waterfall | adventure | nature | history
    description  TEXT,
    address      TEXT,
    distance_km  INT,
    difficulty   TEXT,             -- easy | moderate | hard
    entry_fee    TEXT,
    timings      TEXT,
    image_url    TEXT,
    map_link     TEXT,
    youtube_link TEXT,
    rating       NUMERIC,
    created_at   TIMESTAMPTZ DEFAULT now()
);
"""
