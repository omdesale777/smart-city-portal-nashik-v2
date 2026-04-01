<div align="center">

# Smart City Nashik
### नाशिक स्मार्ट सिटी मॅनेजमेंट पोर्टल

**An integrated web portal centralizing civic services, tourism, and safety reporting for the citizens and tourists of Nashik, Maharashtra.**

[![Made with FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Supabase](https://img.shields.io/badge/Database-Supabase-3ECF8E?style=flat&logo=supabase)](https://supabase.com/)
[![Deployed on Vercel](https://img.shields.io/badge/Frontend-Vercel-black?style=flat&logo=vercel)](https://vercel.com/)
[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue?style=flat&logo=python)](https://python.org/)
[![License MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat)](LICENSE)

</div>

---

## 📌 Overview

The **Smart City Nashik Management Portal** is a full-stack MVP that brings four essential city services under one unified platform — making Nashik safer, cleaner, more efficient, and tourist-friendly.

> 🌊 *Where the sacred Godavari flows through 2,000 years of mythology, ancient temples, Buddhist caves, and India's finest vineyards.*

---

## 🧩 The Four Modules

| # | Module | Name | What it does |
|---|--------|------|-------------|
| 1 | 🕌 **Spiritual & Tourism Hub** | कुंभनगरी नाशिक | Hotels, temples, spiritual spots, Kumbh Mela info |
| 2 | 📋 **Citizen Grievance Portal** | आपले नाशिक आपली जबाबदारी | Report garbage, potholes, broken streetlights, dangerous trees |
| 3 | 🛡️ **Crime Reporting Module** | नाशिक जिल्हा कायद्याचा बालेकिल्ला | Anonymous crime & incident reporting with photo/video evidence |
| 4 | 🗺️ **Bhatakanti Travel Guide** | नाशिक भटकंती | Forts, waterfalls, adventure spots, nature & history explorer |

---

## ⚙️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Fonts** | Playfair Display, DM Sans, Noto Sans Devanagari, Bebas Neue, Cormorant Garamond |
| **Backend** | Python 3.11 + FastAPI |
| **Database** | Supabase (PostgreSQL) |
| **File Storage** | Supabase Storage |
| **Image Processing** | Pillow |
| **Frontend Deploy** | Vercel |
| **Backend Deploy** | Render |

---

## 📁 Project Structure

```
smart-city-portal-nashik-v2/
│
├── frontend/                        ← Static site → Deployed on Vercel
│   ├── index.html                   ← Homepage with 4 module cards
│   ├── vercel.json                  ← Vercel routing config
│   ├── assets/
│   │   ├── css/style.css            ← Shared CSS design tokens & utilities
│   │   └── js/main.js               ← Shared JS helpers (API, cursor, toast)
│   ├── kumbhnagari/
│   │   ├── index.html               ← Spiritual & Tourism Hub
│   │   └── kumbhnagari-api.js       ← API wiring for hotels & spots
│   ├── grievance/
│   │   ├── index.html               ← Citizen Grievance Portal
│   │   └── grievance-api.js         ← API wiring for complaint submission
│   ├── crime/
│   │   ├── index.html               ← Crime Reporting Module
│   │   └── crime-api.js             ← API wiring for crime reports
│   └── tourism/
│       ├── index.html               ← Nashik Bhatakanti Travel Guide
│       └── tourism-api.js           ← API wiring for tourist spots
│
├── backend/                         ← FastAPI app → Deployed on Render
│   ├── main.py                      ← App entry point, CORS, router setup
│   ├── database.py                  ← Supabase client + table definitions
│   ├── requirements.txt             ← Python dependencies (Python 3.11)
│   ├── seed.sql                     ← Seed data for all tables
│   ├── .env.local                   ← 🔑 Supabase keys (never committed)
│   ├── routers/
│   │   ├── grievance.py             ← POST/GET grievance endpoints
│   │   ├── crime.py                 ← POST/GET crime report endpoints
│   │   ├── kumbhnagari.py           ← GET hotels, spiritual spots, events
│   │   └── tourism.py               ← GET tourist spots, categories
│   ├── models/
│   │   └── schemas.py               ← Pydantic request/response models
│   └── storage/
│       └── upload_handler.py        ← Supabase Storage file upload handler
│
├── .gitignore
└── README.md
```

---

## 🚀 Local Development Setup

### Prerequisites

- **Python 3.11** (not 3.12+ due to pydantic-core compatibility)
- A [Supabase](https://supabase.com) account (free)
- VS Code with the **Live Server** extension

### 1. Clone the repo

```bash
git clone git@github.com:omdesale777/smart-city-portal-nashik-v2.git
cd smart-city-portal-nashik-v2
```

### 2. Run the Frontend

Open the project in VS Code → right-click `frontend/index.html` → **Open with Live Server**

Navigate to: `http://localhost:5500`

### 3. Run the Backend

```bash
cd backend

# Create virtual environment with Python 3.11
python3.11 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create your environment file and fill in Supabase credentials
cp .env.example .env.local

# Start the dev server
uvicorn main:app --reload --port 8000
```

API docs (Swagger UI): `http://localhost:8000/docs`

---

## 🗄️ Database Setup (Supabase)

1. Go to [supabase.com](https://supabase.com) → **New Project** → name: `smart-city-nashik`
2. **Settings → API Keys → Legacy tab** → copy the `service_role` key
3. **SQL Editor** → paste and run all `CREATE TABLE` blocks from `backend/database.py`
4. **SQL Editor** → paste and run the full `backend/seed.sql` to populate sample data
5. **Storage** → **New bucket** → name: `uploads` → enable **Public bucket**

---

## ☁️ Deployment

### Frontend → Vercel

```bash
npm i -g vercel
cd frontend
vercel
```

After deploy, update `allow_origins` in `backend/main.py` with your Vercel URL, then redeploy the backend.

### Backend → Render

1. Go to [render.com](https://render.com) → **New Web Service** → connect this GitHub repo
2. **Root Directory**: `backend`
3. **Build Command**: `pip install -r requirements.txt`
4. **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add all environment variables from `.env.local` in the Render dashboard
6. Click **Deploy**

> ⚠️ Free tier on Render spins down after 15 min of inactivity — first request after sleep takes ~30 seconds.

---

## 🔒 Environment Variables

Create `backend/.env.local` with:

```env
SUPABASE_URL=https://your-project-ref.supabase.co
SUPABASE_SERVICE_KEY=eyJ...          # service_role key (Legacy tab)
SUPABASE_ANON_KEY=eyJ...             # anon key (Legacy tab)
SUPABASE_BUCKET=uploads
APP_ENV=development
FRONTEND_URL=http://localhost:5500
```

> ⚠️ `.env.local` is listed in `.gitignore` and will never be committed.

---

## 🛡️ Privacy & Security

- **Anonymous crime reports** — `reporter_phone` is stored as `NULL` when `is_anonymous: true`, enforced at the API layer — not just the frontend
- **Grievances** — contact details used only for NMC follow-up, never publicly exposed
- **No admin panel** in this MVP — add JWT/session-based auth before deploying admin routes publicly
- **CORS** — restricted to your specific Vercel frontend URL only

---

## 🔮 Future Roadmap

- [ ] Real-time complaint status tracking (Supabase Realtime)
- [ ] Admin dashboard for NMC & Nashik Police
- [ ] Marathi / English language toggle
- [ ] Mobile app (React Native)
- [ ] AI chatbot for citizen queries
- [ ] Integration with NMC & Nashik Police APIs
- [ ] Emergency SOS feature with live location
- [ ] Push notifications on complaint resolution

---

## 🎓 Academic Context

| | |
|--|--|
| **College** | Late G. N. Sapkal College of Engineering (LGNSCOE), Nashik |
| **Department** | Computer Engineering |
| **Event** | Impact of AI in Cybersecurity — Project Presentation |
| **Guide** | Prof. R. M. Pandav |
| **Version** | MVP v1.0 |

---


---

<div align="center">

Built with ❤️ for Nashik — *the city of the Godavari, the Kumbh, and the grape.*
Built by -Danny (Om Desale)

⭐ **Star this repo if you found it useful!**

</div>
