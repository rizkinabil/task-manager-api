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
- **Language:** Python 3.14
- **Framework:** FastAPI
- **Server:** Uvicorn (via `fastapi dev src/main.py`)
- **Validation:** Pydantic v2 (with `from_attributes=True` for ORM mode)
- **Config:** pydantic-settings (reads from `.env`)
- **Database:** SQLAlchemy + SQLite (`src/tasks.db`, gitignored)
- **Auth:** `passlib[bcrypt]` + `python-jose[cryptography]` (Stage 4)
- **Formatter:** Black (`black src/` or auto on save in VS Code)

---

## Project Structure
Follows [zhanymkanov/fastapi-best-practices](https://github.com/zhanymkanov/fastapi-best-practices) — domain-driven layout.

### Current (Stage 3 complete)
```
FastAPI/
├── src/
│   ├── __init__.py
│   ├── main.py           ← FastAPI app + router + Base.metadata.create_all
│   ├── config.py         ← pydantic-settings, reads from .env
│   ├── database.py       ← SQLAlchemy engine, SessionLocal, Base
│   ├── pagination.py     ← PaginatedTaskResponse schema
│   └── tasks/
│       ├── __init__.py
│       ├── router.py     ← HTTP endpoints, Depends(get_db), Depends(FilterParams)
│       ├── schemas.py    ← Pydantic models (TaskCreate, TaskUpdate, TaskResponse)
│       ├── models.py     ← SQLAlchemy Task ORM model
│       ├── service.py    ← business logic using db: Session
│       └── dependencies.py ← get_db(), FilterParams class
├── .editorconfig         ← 4-space indent for all editors
├── .vscode/settings.json ← Black formatter on save
├── .env                  ← environment variables (gitignored)
├── .gitignore            ← excludes .claude/, .env, __pycache__, *.db
├── CONTEXT.md            ← this file
└── requirements.txt
```

### After Stage 4 (target structure)
```
src/
├── auth/
│   ├── __init__.py
│   ├── router.py         ← /auth/register, /auth/login
│   ├── schemas.py        ← UserCreate, UserResponse, TokenResponse
│   ├── service.py        ← register/login logic, password hashing, JWT
│   └── dependencies.py  ← get_current_user (JWT guard)
└── users/
    ├── __init__.py
    └── models.py         ← User SQLAlchemy model
```

**When adding a new domain, always mirror this structure:**
`__init__.py`, `router.py`, `schemas.py`, `models.py`, `service.py`, `dependencies.py`

---

## Key Conventions
- **API prefix:** `/api/v1` (set in each `router.py`, not `main.py`)
- **No trailing slash** on endpoints (`/tasks` not `/tasks/`)
- **Enums use `str, Enum`** — serializes to plain string in JSON
- **`TaskUpdate` fields all optional** — use `exclude_unset=True` in service
- **`TaskResponse`** has `model_config = {"from_attributes": True}` — enables ORM mode
- **Internal model vs response model:** SQLAlchemy `Task` (ORM) → converted via `TaskResponse.model_validate(t.model_dump())` in router
- **DB session:** injected via `Depends(get_db)` — never create sessions manually in router
- **FilterParams:** grouped query params as a class in `dependencies.py`, used as `Depends(FilterParams)`
- **`*.db` files** are gitignored — never commit the database file
- **HTTP status codes:** `201` create, `204` delete, `400` bad request, `401` unauthorized, `404` not found, `422` validation
- **Commit style:** `feat:`, `fix:`, `chore:`, `refactor:`, `docs:` prefixes
- **Indentation:** 4 spaces (enforced by `.editorconfig` + Black formatter)

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
UUID path params, HTTPException, domain-driven project structure.

### Stage 2 — Filtering & Pagination ✅ Complete
| Issue | Feature | Status |
|---|---|---|
| #6 | Add `priority` and `status` enum fields | ✅ Done |
| #7 | Filter tasks by `status` and `priority` | ✅ Done |
| #8 | Paginate task list (`page`, `limit`) | ✅ Done |

**What was learned:** `str, Enum`, query params, `Query()` validation, `FilterParams`
class pattern, `PaginatedResponse` schema, `model_dump()` for type conversion.

### Stage 3 — Real Database ✅ Complete
| Issue | Feature | Status |
|---|---|---|
| #9 | SQLAlchemy setup + Task DB model | ✅ Done |
| #10 | Alembic migrations | ⏭️ Skipped (using `create_all`) |
| #11 | DB session dependency | ✅ Done |
| #12 | Refactor service to use DB | ✅ Done |

**What was learned:** SQLAlchemy ORM, `DeclarativeBase`, FK columns, `SessionLocal`,
`yield` dependency pattern, `db.add/commit/refresh`, ORM query filters, `setattr`
for partial updates, `from_attributes=True` for ORM→Pydantic conversion.

### Stage 4 — Authentication 🔄 In Progress
| Issue | Feature | Status |
|---|---|---|
| #13 | Auth domain + User model + `owner_id` FK on Task | 📋 Backlog |
| #14 | `POST /api/v1/auth/register` | 📋 Backlog |
| #15 | `POST /api/v1/auth/login` → JWT token | 📋 Backlog |
| #16 | Protect task routes + task ownership | 📋 Backlog |

**What will be learned:** Password hashing (bcrypt), JWT generation/verification,
`Depends()` for auth guards, `401` handling, FK relationships, data ownership.

**New dependencies for Stage 4:**
```
passlib[bcrypt]
python-jose[cryptography]
```

**New `.env` keys for Stage 4:**
```
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## GitHub Setup
- **Repo:** https://github.com/rizkinabil/task-manager-api
- **Branch:** `main`
- **Project board:** Kanban with Backlog / In Progress / In Review / Done
- **Labels:** `stage-1`, `stage-2`, `stage-3`, `stage-4`, `feature`, `qa`
- **GitHub CLI (`gh`):** installed, authenticated as `rizkinabil`
  - Path on Windows: `C:/Program Files/GitHub CLI`
  - Always prepend: `export PATH="$PATH:/c/Program Files/GitHub CLI"` before `gh` commands

---

## How to Run
```bash
# Install dependencies
pip install -r requirements.txt

# Start dev server (DB tables auto-created on startup)
fastapi dev src/main.py

# Docs
http://localhost:8000/docs
```

---

## Notes for the AI Agent
- The human is a beginner coming from a non-Python background — explain new concepts
- Always read the actual code files before doing QA review — never assume
- Don't give full solutions immediately — give hints first, let them try
- When QA fails, list specific issues clearly with line numbers
- Close GitHub issues only after QA explicitly passes
- After each stage completes: commit, push, update CONTEXT.md
- The human responds well to the structured `[USER]` → `[PM]` → `[QA]` format
- Keep responses concise — the human prefers direct communication
- Black formatter is configured — remind to run `black src/` if indentation looks off
