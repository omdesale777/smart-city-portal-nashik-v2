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
    Supports both old (eyJ...) and new (sb_secret_...) Supabase key formats.
    Uses service-role/secret key to bypass Row Level Security for backend writes.
    Never expose this key to the frontend.
    """
    url = os.environ.get("SUPABASE_URL")

    # Support both old service_role key and new sb_secret_ key format
    key = (
        os.environ.get("SUPABASE_SERVICE_KEY") or
        os.environ.get("SUPABASE_SECRET_KEY")
    )

    if not url or not key:
        raise RuntimeError(
            "\n\n❌  Missing Supabase credentials in .env file.\n"
            "    Required variables:\n"
            "      SUPABASE_URL=https://xxxx.supabase.co\n"
            "      SUPABASE_SERVICE_KEY=eyJ...  (from Legacy anon/service_role tab)\n"
            "    OR (new key format):\n"
            "      SUPABASE_SECRET_KEY=sb_secret_...  (from Secret keys section)\n"
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
    photos          TEXT[],
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
    reporter_phone   TEXT,
    media            TEXT[],
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
    price_from  INT,
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

-- 5. Spiritual Events
CREATE TABLE spiritual_events (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name        TEXT NOT NULL,
    icon        TEXT,
    when_text   TEXT,
    description TEXT,
    created_at  TIMESTAMPTZ DEFAULT now()
);

-- 6. Tourist Spots (Bhatakanti)
CREATE TABLE tourist_spots (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name         TEXT NOT NULL,
    category     TEXT NOT NULL,
    description  TEXT,
    address      TEXT,
    distance_km  INT,
    difficulty   TEXT,
    entry_fee    TEXT,
    timings      TEXT,
    image_url    TEXT,
    map_link     TEXT,
    youtube_link TEXT,
    rating       NUMERIC,
    created_at   TIMESTAMPTZ DEFAULT now()
);
"""