# JobSeeker AI Agent — Design Spec

## Overview
AI-powered job search agent targeting Malaysian hospitality (餐飲) industry on JobStreet. Mobile-first webapp with Flask backend, freemium pricing.

## Architecture

```
User (mobile browser) ←→ Flask API ←→ SQLite
                        ↕
                    Scraper Scheduler (APScheduler) ←→ JobStreet
                        ↕
                    LLM Agent (Claude API) → resume tailoring, cover letter, matching
```

## Directory Structure

```
jobseekr/
├── backend/
│   ├── app.py                 # Flask entry
│   ├── config.py              # Config
│   ├── database.py            # SQLite init + helpers
│   └── models/
│       ├── __init__.py
│       └── schema.sql         # DDL
│   ├── scrapers/
│   │   ├── __init__.py
│   │   ├── base.py            # BaseScraper
│   │   └── jobstreet.py       # JobStreet scraper
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── matcher.py         # LLM matching
│   │   ├── resume_tailor.py   # Resume tailoring
│   │   └── cover_letter.py    # Cover letter gen
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py            # Register/login/logout
│   │   ├── jobs.py            # Job browse/search
│   │   ├── profile.py         # Profile CRUD
│   │   └── applications.py    # Apply + tracking
│   └── requirements.txt
├── frontend/                  # Mobile-first SPA (CSS-only)
└── tests/
    └── test_api.py
```

## Database Schema

- `users` — id, email, password_hash, name, phone, plan (free/paid), created_at
- `profiles` — user_id, resume_text, skills (JSON), preferred_location, preferred_category
- `jobs` — id, platform, platform_id, title, company, location, category, description, url, posted_at, scraped_at
- `applications` — id, user_id, job_id, status (pending/sent/rejected), custom_resume, cover_letter, applied_at

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | /api/auth/register | Register user |
| POST | /api/auth/login | Login (session) |
| POST | /api/auth/logout | Logout |
| GET | /api/jobs | List jobs (filter: category, location, keyword) |
| GET | /api/jobs/<id> | Job detail |
| POST | /api/jobs/<id>/match | LLM match score |
| GET | /api/profile | Get profile |
| PUT | /api/profile | Update profile |
| POST | /api/applications | Apply (auto tailor) |
| GET | /api/applications | Application history |

## Freemium Split

| Feature | Free | Paid |
|---------|------|------|
| Browse jobs | ✅ | ✅ |
| Manual apply | ✅ | ✅ |
| Resume suggestions | ✅ | ✅ |
| Auto match alerts | ❌ | ✅ |
| Auto tailor resume | ❌ | ✅ |
| Auto cover letter | ❌ | ✅ |
| Batch apply | ❌ | ✅ |
| Track applications | ❌ | ✅ |

## Tech Stack

- **Backend:** Flask, SQLite, APScheduler
- **LLM:** Claude API (Anthropic)
- **Auth:** Session-based (flask.session)
- **Scraping:** requests + BeautifulSoup (static pages) or Playwright (JS-rendered)
