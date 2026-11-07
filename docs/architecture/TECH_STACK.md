# Technology Stack and Environment Specification

## 1. Overview
This document specifies the approved technology stack, language versions, database engines, and runtime dependencies for the **Intelligent Data Management and Operational Analytics for Autonomous Post-Harvest Material Handling Systems** DBMS project.

---

## 2. Environment Audit and Runtime Verification

A system audit performed during repository initialization on the host system (Windows 11) detected the following:

| Tool | Status | Detected Version | Notes / Compatibility |
| :--- | :--- | :--- | :--- |
| **Operating System** | Detected | Windows 11 | Host OS |
| **Python** | Detected | `3.13.14` | Supported for FastAPI, SQLAlchemy 2.0+, and PyMongo |
| **Git** | Detected | `2.55.0.windows.1` | Source control ready |
| **Node.js** | Detected | `v24.15.0` | Node LTS runtime for Vite / React build tooling |
| **npm** | Detected | `11.6.2` | Frontend package manager |
| **Docker Desktop** | Not Detected | Not on PATH | Optional. Docker Compose template provided |
| **MySQL Server** | Not Detected | Not on PATH | Target: MySQL 8.4 LTS (native or Docker container) |
| **MongoDB Server** | Not Detected | Not on PATH | Target: MongoDB 8.0 Community (native or Docker container) |

---

## 3. Technology Selections and Justification

### 3.1 Frontend Stack
- **Framework**: **React 18 / 19** with **TypeScript**
  - *Rationale*: Type-safe component development, explicit interface definitions matching backend Pydantic schemas.
- **Build Tool**: **Vite**
  - *Rationale*: Sub-second HMR, optimized production builds, standard modern frontend tooling.
- **Styling**: **Tailwind CSS**
  - *Rationale*: Utility-first, responsive grid and layout system for dense dashboard views.
- **Routing**: **React Router (v6+)**
  - *Rationale*: Client-side multi-page routing across the 9 dashboard views.
- **Data Fetching & State**: **TanStack Query (React Query v5)**
  - *Rationale*: Automatic query caching, background re-fetching, integrated loading/error states, and pagination support.
- **Charts & Visualizations**: **Recharts**
  - *Rationale*: Declarative SVG-based charting library built specifically for React, supporting donut, bar, and line operational charts.

### 3.2 Backend Stack
- **Framework**: **FastAPI**
  - *Rationale*: High-performance asynchronous REST framework, automatic OpenAPI documentation generation (`/docs`), and native dependency injection.
- **Data Validation & Serialization**: **Pydantic (v2+)**
  - *Rationale*: Strict type checking, automatic coercion, clear error messages, and schema export.
- **ORM & SQL Layer**: **SQLAlchemy (v2.0+)**
  - *Rationale*: Robust relational abstraction, declarative mapping, transactional safety, and connection pooling.
- **MySQL Driver**: **PyMySQL (`mysql+pymysql://`)**
  - *Rationale*: Pure-Python driver compatible with Python 3.13 on Windows 11 without requiring Microsoft C++ Build Tools (which `mysqlclient` requires). Paired with `cryptography` for `caching_sha2_password` authentication support.
- **MongoDB Driver**: **PyMongo (v4.8+)**
  - *Rationale*: Standard official Python driver for MongoDB Community Server 8.0.
- **Test Framework**: **pytest**
  - *Rationale*: Standard Python testing framework for unit, integration, and mock database tests.

### 3.3 Database Layer
- **Relational Database**: **MySQL 8.4 LTS**
  - *Purpose*: Authoritative relational storage for sessions, tasks, decisions, operations, devices, and structured system events.
  - *Default Port*: `3306`
- **Document Database**: **MongoDB Community Server 8.0**
  - *Purpose*: Flexible document storage for vision detection records, AI model inference configurations, and telemetry streams.
  - *Default Port*: `27017`

---

## 4. Architectural Constraints and Disallowed Technologies
To maintain project focus, avoid unnecessary complexity, and ensure reproducibility:
- **Single Monolith Gateway**: Exactly one FastAPI backend application and one React frontend. No secondary backend frameworks (e.g. Django, Flask).
- **No Streamlit**: Streamlit is prohibited for the primary operational dashboard; the React dashboard is the authoritative frontend.
- **No Heavy Distributed Middleware**: Redis, Apache Kafka, RabbitMQ, Celery, and Elasticsearch are strictly excluded.
- **No Cloud Services**: AWS, GCP, Azure, or Cloudflare services are not used for local development.
- **No Object Storage**: MinIO or AWS S3 are not used; vision data is limited to detection metadata.

---

## 5. Target Dependency Specifications

### Backend (`backend/requirements.txt` - Target Pins)
```text
fastapi>=0.115.0,<0.116.0
uvicorn[standard]>=0.32.0,<0.33.0
pydantic>=2.9.0,<3.0.0
pydantic-settings>=2.6.0,<3.0.0
sqlalchemy>=2.0.36,<2.1.0
pymysql>=1.1.1,<1.2.0
cryptography>=43.0.0,<44.0.0
pymongo>=4.9.0,<5.0.0
python-dotenv>=1.0.1,<2.0.0
pytest>=8.3.0,<9.0.0
pytest-asyncio>=0.24.0,<0.25.0
httpx>=0.27.0,<0.28.0
```

### Frontend (`frontend/package.json` - Target Dependencies)
```json
{
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "react-router-dom": "^6.26.0",
    "@tanstack/react-query": "^5.59.0",
    "recharts": "^2.13.0",
    "lucide-react": "^0.453.0",
    "clsx": "^2.1.1",
    "tailwind-merge": "^2.5.4"
  },
  "devDependencies": {
    "@types/react": "^18.3.11",
    "@types/react-dom": "^18.3.10",
    "@vitejs/plugin-react": "^4.3.2",
    "typescript": "^5.6.3",
    "vite": "^5.4.9",
    "tailwindcss": "^3.4.14",
    "postcss": "^8.4.47",
    "autoprefixer": "^10.4.20",
    "eslint": "^9.13.0"
  }
}
```

