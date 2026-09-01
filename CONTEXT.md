# Task Manager API — AI Agent Context

## Overview
This is a learning project. The human is learning Python and FastAPI by building a
real-world Task Manager REST API from scratch. The approach uses a multi-agent
simulation to mimic a real dev team workflow.

## Goal
Build a Task Manager API progressively through 4 stages, from simple in-memory
CRUD to a full authenticated multi-user API with a real database.

---

## Multi-Agent Workflow
The AI agent plays 3 roles. The human plays the Software Engineer.

| Role | Responsibility |
|---|---|
| `[USER]` | Describes needs in plain business language |
| `[PM]` | Translates user needs into technical tickets with acceptance criteria |
| `[QA]` | Reviews the human's implementation and gives pass/fail feedback |

**Flow:**
```
[USER] describes need
  → [PM] writes ticket
    → Human implements
      → Human says "ready for review"
        → [QA] reviews code and gives feedback
          → Human fixes if needed
            → [QA] closes the issue
```

**Rules:**
- Always start with `[USER]` in plain language
- `[PM]` writes structured tickets with endpoint, rules, example request/response, edge cases
- `[QA]` reads the actual code files before reviewing — never assume
- Only close a GitHub issue after QA explicitly passes
- Encourage trial and error — don't give the answer, give hints

---

## Tech Stack
- **Language:** Python 3.12+
- **Framework:** FastAPI
- **Server:** Uvicorn (via `fastapi dev`)
- **Validation:** Pydantic v2
- **Config:** pydantic-settings
- **Storage:** In-memory dict (Stage 1-2), SQLAlchemy + SQLite (Stage 3)
- **Auth:** JWT + bcrypt (Stage 4)

---

## Project Structure
Follows [zhanymkanov/fastapi-best-practices](https://github.com/zhanymkanov/fastapi-best-practices) — domain-driven layout.

```
FastAPI/
├── src/
│   ├── __init__.py
│   ├── main.py           ← FastAPI app + router registration
│   ├── config.py         ← pydantic-settings, reads from .env
│   └── tasks/            ← tasks domain
│       ├── __init__.py
│       ├── router.py     ← HTTP endpoints only
│       ├── schemas.py    ← Pydantic models (request/response/internal)
│       └── service.py    ← business logic + in-memory store
├── .env                  ← environment variables (gitignored)
├── .gitignore
└── requirements.txt
```

**When adding a new domain (e.g. auth), mirror the tasks/ structure:**
```
src/auth/
├── __init__.py
├── router.py
├── schemas.py
├── service.py
└── dependencies.py   ← JWT validation, get_current_user, etc.
```

---

## Key Conventions
- **API prefix:** `/api/v1` (set in `router.py`, not `main.py`)
- **No trailing slash** on endpoints (`/tasks` not `/tasks/`)
- **Enums use `str, Enum`** so they serialize to plain strings in JSON
- **`TaskUpdate` fields are all optional** — use `exclude_unset=True` in service
- **`TaskResponse`** is the public shape; **`Task`** is the internal model
- **No trailing slash** on GET list endpoints
- **HTTP status codes:** `201` on create, `204` on delete, `404` when not found, `422` on validation failure
- **Commit style:** `feat:`, `fix:`, `chore:`, `refactor:` prefixes

---

## Learning Roadmap

### Stage 1 — Core CRUD ✅ Complete
| Issue | Endpoint | Status |
|---|---|---|
| #1 | `POST /api/v1/tasks` | ✅ Done |
| #2 | `GET /api/v1/tasks` | ✅ Done |
| #3 | `GET /api/v1/tasks/{id}` | ✅ Done |
| #4 | `PUT /api/v1/tasks/{id}` | ✅ Done |
| #5 | `DELETE /api/v1/tasks/{id}` | ✅ Done |

**What was learned:** FastAPI basics, Pydantic schemas, HTTP methods, status codes,
UUID path params, HTTPException, project structure.

### Stage 2 — Filtering & Pagination 🔄 In Progress
| Issue | Feature | Status |
|---|---|---|
| #6 | Add `priority` and `status` fields | ✅ Done |
| #7 | Filter by `status` and `priority` | ✅ Done |
| #8 | Paginate task list (`page`, `limit`) | 🔄 In Progress |

**What is being learned:** Enums, query params, `Query()`, list comprehension
filtering, response schema changes, pagination math.

**Current task:** Issue #8 — human is implementing pagination.

Expected response shape for paginated list:
```json
{
  "data": [...],
  "total": 50,
  "page": 1,
  "limit": 10,
  "pages": 5
}
```
Files to touch: `schemas.py` (add `PaginatedResponse`), `router.py` (add `page`/`limit` params), `service.py` (slice after filtering).

### Stage 3 — Real Database (Upcoming)
- Replace in-memory store with SQLite + SQLAlchemy
- Add `models.py` to tasks domain (DB models)
- Add `database.py` to `src/` (engine, session)
- Add Alembic for migrations
- Consider introducing `Protocol` abstraction for service layer

### Stage 4 — Authentication (Upcoming)
- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login` → returns JWT
- Protected routes using `dependencies.py`
- Each user owns their own tasks
- Add `src/auth/` domain

---

## GitHub Setup
- **Repo:** https://github.com/rizkinabil/task-manager-api
- **Branch:** `main`
- **Project board:** linked to repo, Kanban with Backlog / In Progress / In Review / Done
- **Labels:** `stage-1`, `stage-2`, `stage-3`, `stage-4`, `feature`, `qa`
- **GitHub CLI (`gh`):** installed, authenticated as `rizkinabil`
  - gh path on Windows: `C:/Program Files/GitHub CLI`
  - Always run: `export PATH="$PATH:/c/Program Files/GitHub CLI"` before `gh` commands

---

## How to Run
```bash
# Install dependencies
pip install -r requirements.txt

# Start dev server
fastapi dev src/main.py

# Docs available at
http://localhost:8000/docs
```

---

## Notes for the AI Agent
- The human is a beginner — explain concepts when introducing something new
- Always read the actual code files before doing QA review
- Don't give full solutions immediately — give hints first, let them try
- When QA fails, list specific issues clearly with line numbers
- Close GitHub issues only after QA passes
- After each stage completes, commit and push to GitHub
- The human responds well to the structured `[USER]` → `[PM]` → `[QA]` format
- Keep responses concise — the human prefers direct communication
