"""
Smart City Nashik — FastAPI Backend
Entry point: main.py

Run locally:
    uvicorn main:app --reload --port 8000

Deployed on Render (free tier):
    Start command: uvicorn main:app --host 0.0.0.0 --port $PORT
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from routers import grievance, crime, kumbhnagari, tourism


# ── Lifespan (startup / shutdown) ──────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("✅ Smart City Nashik API starting up…")
    yield
    print("🛑 Smart City Nashik API shutting down…")


# ── App ────────────────────────────────────────────────────────
app = FastAPI(
    title="Smart City Nashik API",
    description=(
        "Backend for the Smart City Nashik Management Portal. "
        "Provides endpoints for citizen grievances, crime reporting, "
        "spiritual tourism (Kumbhnagari), and the Bhatakanti travel guide."
    ),
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)


# ── CORS ───────────────────────────────────────────────────────
# Update `allow_origins` with your actual Vercel frontend URL before deploying.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",          # VS Code Live Server
        "http://127.0.0.1:5500",
        "http://localhost:3000",
        "https://smart-city-nashik.vercel.app",  # ← replace with your Vercel URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Routers ────────────────────────────────────────────────────
app.include_router(grievance.router,    prefix="/api/grievances",   tags=["Grievance Portal"])
app.include_router(crime.router,        prefix="/api/crime-reports", tags=["Crime Reporting"])
app.include_router(kumbhnagari.router,  prefix="/api/kumbhnagari",  tags=["Kumbhnagari Tourism"])
app.include_router(tourism.router,      prefix="/api/tourism",       tags=["Bhatakanti Travel Guide"])


# ── Health check ───────────────────────────────────────────────
@app.get("/", tags=["Health"])
def root():
    return {
        "status": "ok",
        "project": "Smart City Nashik Management Portal",
        "version": "1.0.0",
        "modules": ["grievance", "crime", "kumbhnagari", "tourism"],
    }


@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy"}
