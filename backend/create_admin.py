"""
create_admins.py — Run this ONCE to create admin accounts in Supabase.

Usage:
    cd backend
    source venv/bin/activate
    python create_admins.py

Change the passwords below before running.
"""

import os
import sys
from dotenv import load_dotenv
from passlib.context import CryptContext

load_dotenv(".env.local")

from supabase import create_client

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_admin(sb, username: str, password: str, role: str):
    """Insert one admin record with a bcrypt-hashed password."""
    # Check if already exists
    existing = sb.table("admins").select("id").eq("username", username).execute()
    if existing.data:
        print(f"⚠️  Admin '{username}' already exists — skipping.")
        return

    hashed = pwd_ctx.hash(password)
    result = sb.table("admins").insert({
        "username":      username,
        "password_hash": hashed,
        "role":          role,
    }).execute()

    if result.data:
        print(f"✅ Created admin: username='{username}' role='{role}'")
    else:
        print(f"❌ Failed to create admin: '{username}'")


if __name__ == "__main__":
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_SERVICE_KEY") or os.environ.get("SUPABASE_SECRET_KEY")

    if not url or not key:
        print("❌ Missing SUPABASE_URL or SUPABASE_SERVICE_KEY in .env.local")
        sys.exit(1)

    sb = create_client(url, key)

    # ── Set your passwords here ───────────────────────────────────
    # Use strong passwords in production!
    admins = [
        {
            "username": "nmc_nashik",
            "password": "NMC@Nashik2024",      # ← change this
            "role":     "nmc",
        },
        {
            "username": "police_nashik",
            "password": "Police@Nashik2024",    # ← change this
            "role":     "police",
        },
    ]
    # ─────────────────────────────────────────────────────────────

    print("\n🔐 Creating admin accounts...\n")
    for admin in admins:
        create_admin(sb, admin["username"], admin["password"], admin["role"])

    print("\n✅ Done. Keep these credentials safe — they are NOT stored in plain text.\n")