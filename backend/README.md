# Backend Service — FastAPI Gateway and Database Persistence
**Developer Owner**: Rahul (Backend and Database Integration Developer)

---

## 1. Overview
The backend application is built using **FastAPI** on Python 3.13+. It acts as the operational persistence gateway, business logic validator, and data retrieval service for the **Post-Harvest DBMS**.

It integrates with:
- **MySQL 8.4 LTS** via **SQLAlchemy 2.0+** and pure-Python **PyMySQL** driver.
- **MongoDB Community Server 8.0** via **PyMongo**.

---

## 2. Directory Structure
```text
backend/
├── app/
│   ├── api/             # FastAPI routers & endpoint definitions
│   ├── core/            # Configuration (pydantic-settings), logging, security
│   ├── database/        # Database session factories (MySQL SQLAlchemy, MongoDB PyMongo)
│   ├── models/          # SQLAlchemy relational ORM models
│   ├── repositories/    # Database query execution classes (SQL & NoSQL)
│   ├── schemas/         # Pydantic request/response validation schemas
│   ├── services/        # Business logic, simulation coordination, and workflows
│   └── main.py          # FastAPI application factory and lifespan events
├── tests/               # Pytest unit, repository, and API route tests
├── requirements.txt     # Pinned Python package dependencies
└── README.md            # This documentation file
```

---

## 3. Local Development Setup (Windows 11)

### Step 1: Create and Activate Virtual Environment
```powershell
# From project root
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### Step 2: Install Dependencies
```powershell
pip install -r backend/requirements.txt
```

### Step 3: Run FastAPI Development Server
```powershell
uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```
Interactive API documentation will be available at:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

---

## 4. Running Automated Tests
```powershell
pytest backend/tests -v
```
All tests must execute against isolated test databases or mock fixtures. Never run destructive cleanup against primary development databases.

