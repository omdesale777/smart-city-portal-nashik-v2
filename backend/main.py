"""
Smart City Nashik — FastAPI Backend
Entry point: main.py

Run locally:
    uvicorn main:app --reload --port 8000
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from routers import grievance, crime, kumbhnagari, tourism, admin


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("✅ Smart City Nashik API starting up…")
    yield
    print("🛑 Smart City Nashik API shutting down…")


app = FastAPI(
    title="Smart City Nashik API",
    description="Backend for the Smart City Nashik Management Portal.",
    version="1.0.0",
    lifespan=lifespan,
)

# ── CORS ──────────────────────────────────────────────────────────
# Regex matches:
#   - any localhost / 127.0.0.1 port (local dev: Live Server, http.server, Vite, …)
#   - any https://<anything>.vercel.app origin (production + preview deploys)
# Add explicit origins to `allow_origins` for non-Vercel production hosts.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "null",   # file:// protocol for local testing
    ],
    allow_origin_regex=(
        r"^(?:"
        r"http://(?:localhost|127\.0\.0\.1)(?::\d+)?"
        r"|https://[a-zA-Z0-9-]+\.vercel\.app"
        r")$"
    ),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ────────────────────────────────────────────────────────
app.include_router(grievance.router,   prefix="/api/grievances",    tags=["Grievance Portal"])
app.include_router(crime.router,       prefix="/api/crime-reports",  tags=["Crime Reporting"])
app.include_router(kumbhnagari.router, prefix="/api/kumbhnagari",   tags=["Kumbhnagari Tourism"])
app.include_router(tourism.router,     prefix="/api/tourism",        tags=["Bhatakanti Travel Guide"])
app.include_router(admin.router,       prefix="/api/admin",          tags=["Admin"])

# ── Health ─────────────────────────────────────────────────────────
@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "version": "1.0.0"}

@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy"}