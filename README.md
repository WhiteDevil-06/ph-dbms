# Intelligent Data Management and Operational Analytics for Autonomous Post-Harvest Material Handling Systems

[![Project Phase](https://img.shields.io/badge/Phase-Prototype_Simulation-orange.svg)]()
[![License](https://img.shields.io/badge/License-Academic_Research-blue.svg)]()

## 1. Executive Summary

This project implements a dedicated data management, persistence, operational monitoring, and analytics layer for an autonomous post-harvest agricultural material handling robotics system. 

In automated post-harvest operations, agricultural produce is picked, inspected, sorted, and routed through autonomous platforms and manipulators. The robotic workflow proceeds as follows:

```text
Vision Module → Object Detection → Localization → Decision Logic → Navigation → Manipulation → Verification
```

### The System Boundary
The **Post-Harvest DBMS** is strictly an **operational analytics and persistence subsystem**. 
- **It is NOT the robot's real-time command-and-control system.**
- It does **not** perform motor driving, manipulator trajectory planning, or safety-critical hardware interrupts.
- It **captures, indexes, and analyzes** operational records, decisions, detection metadata, system events, and equipment status.

> [!IMPORTANT]
> **Simulation-Only Phase**: The physical robotic hardware is actively under construction. For this implementation phase, all operational data is supplied by an internal, deterministic **Simulated Data Generator**. No live field connections or real robot hardware telemetry are active. All simulated records carry explicit provenance indicators.

---

## 2. Project Team and Module Ownership

| Name | Role | Core Ownership | Role Brief |
| :--- | :--- | :--- | :--- |
| **Rakshith Raghavendra** | Project Lead & Database Architect | Architecture oversight, ER model, Relational Schema (MySQL 8.4), Migrations, Decision Log | [.agents/roles/RAKSHITH_RAGHAVENDRA.md](.agents/roles/RAKSHITH_RAGHAVENDRA.md) |
| **Ramcharan** | Frontend & Dashboard Developer | React (Vite/TS/Tailwind) Dashboard, UI State, Recharts Visualizations, API consumption | [.agents/roles/RAMCHARAN.md](.agents/roles/RAMCHARAN.md) |
| **Rahul** | Backend & Database Integration | FastAPI Backend, MySQL & MongoDB Repositories, Pydantic Schemas, Simulator Integration | [.agents/roles/RAHUL.md](.agents/roles/RAHUL.md) |

---

## 3. High-Level Architecture

```text
[ Seeded Data Simulator / Test Harness ]
                   ↓ (JSON / REST Payloads)
       [ FastAPI Application Layer ]
        ├── Validation & Core Services
        ├── MySQL SQLAlchemy Repository  ──→  [ MySQL 8.4 LTS ] (Sessions, Tasks, Operations, Devices)
        └── MongoDB PyMongo Repository   ──→  [ MongoDB 8.0 ] (Detections, Inference, Telemetry Logs)
                   ↓ (REST HTTP/JSON API)
       [ React / TypeScript Dashboard ]
        ├── Overview & Session Monitor
        ├── Detection Metadata & Analytics
        └── Persistent "SIMULATION DATA" Indicator
```

---

## 4. Documentation Index

Comprehensive documentation is organized inside `docs/`:

- **Project Foundations**:
  - [PROJECT_CONTEXT.md](docs/project/PROJECT_CONTEXT.md): System context, operational background, and boundaries.
  - [SCOPE_AND_OBJECTIVES.md](docs/project/SCOPE_AND_OBJECTIVES.md): Project goals, deliverables, and out-of-scope boundaries.
  - [REQUIREMENTS.md](docs/project/REQUIREMENTS.md): Functional and non-functional specifications.
  - [DASHBOARD_SPECIFICATION.md](docs/project/DASHBOARD_SPECIFICATION.md): UI pages, layout, and component specifications.
- **Architecture & Technology**:
  - [SYSTEM_ARCHITECTURE.md](docs/architecture/SYSTEM_ARCHITECTURE.md): Multi-tier architecture and data flows.
  - [TECH_STACK.md](docs/architecture/TECH_STACK.md): Pinned stack, environment compatibility, and justification.
  - [ARCHITECTURE_AUDIT.md](docs/architecture/ARCHITECTURE_AUDIT.md): Detailed audit of source diagrams and discrepancies.
- **Database & Data Modeling**:
  - [DIAGRAM_INVENTORY.md](docs/diagrams/DIAGRAM_INVENTORY.md): Source diagram inventory and checksums.
  - [ER_TO_RELATIONAL_MAPPING.md](docs/database/ER_TO_RELATIONAL_MAPPING.md): Detailed entity and relationship mapping.
  - [DATA_OWNERSHIP_MATRIX.md](docs/database/DATA_OWNERSHIP_MATRIX.md): SQL vs NoSQL store allocation matrix.
  - [MYSQL_DESIGN.md](docs/database/MYSQL_DESIGN.md): Relational tables, indexes, constraints, and audit log.
  - [MONGODB_DESIGN.md](docs/database/MONGODB_DESIGN.md): Document collections, JSON schemas, and indexing.
- **Interfaces & Operations**:
  - [API_CONTRACT.md](docs/api/API_CONTRACT.md): FastAPI REST endpoints, schemas, and error responses.
  - [SIMULATION_SPEC.md](docs/simulation/SIMULATION_SPEC.md): Deterministic generator logic, states, and scenarios.
  - [DECISION_LOG.md](docs/decisions/DECISION_LOG.md): Architectural and schema decisions log.
  - [TEAM_RESPONSIBILITIES.md](docs/team/TEAM_RESPONSIBILITIES.md): Role boundaries and collaboration workflow.

---

## 5. Local Setup & Quickstart

See [TECH_STACK.md](docs/architecture/TECH_STACK.md) for full environmental prerequisite instructions.

### 1. Prerequisites Check
- Windows 11
- Python 3.13+ installed
- Node.js LTS (v24+) & npm installed
- MySQL 8.4 LTS & MongoDB 8.0 (native Windows services or Docker Desktop)

### 2. Environment Setup
```powershell
# Copy environment template
Copy-Item .env.example .env

# Create and activate Python virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1

# Install backend dependencies
pip install -r backend/requirements.txt
```

### 3. Run Deterministic Simulation Data Generator
```powershell
# Synthesize simulated data in dry-run mode (or insert if DBs are running)
python -m simulator.generators.main --seed 42 --scale demo --mode dry-run
```

### 4. Run Automated Test Suite
```powershell
pytest backend/tests -v
```

### 5. Run FastAPI Backend Server
```powershell
uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```
- Swagger UI: `http://127.0.0.1:8000/docs`
- Health check: `http://127.0.0.1:8000/health`

---

## 6. Contributing
All code changes must be submitted via pull request on a dedicated feature branch. See [CONTRIBUTING.md](CONTRIBUTING.md) for rules and branch naming conventions.
