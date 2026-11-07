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
| **Rakshith Raghavendra** | Project Lead & Database Architect | Architecture oversight, ER model, Relational Schema (MySQL 8.4), Migrations, Decision Log | [.agents/roles/RAKSHITH_RAGHAVENDRA.md](file:///c:/Users/raksh/OneDrive/Desktop/Post-Harvest-DBMS/.agents/roles/RAKSHITH_RAGHAVENDRA.md) |
| **Ramcharan** | Frontend & Dashboard Developer | React (Vite/TS/Tailwind) Dashboard, UI State, Recharts Visualizations, API consumption | [.agents/roles/RAMCHARAN.md](file:///c:/Users/raksh/OneDrive/Desktop/Post-Harvest-DBMS/.agents/roles/RAMCHARAN.md) |
| **Rahul** | Backend & Database Integration | FastAPI Backend, MySQL & MongoDB Repositories, Pydantic Schemas, Simulator Integration | [.agents/roles/RAHUL.md](file:///c:/Users/raksh/OneDrive/Desktop/Post-Harvest-DBMS/.agents/roles/RAHUL.md) |

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
  - [PROJECT_CONTEXT.md](file:///c:/Users/raksh/OneDrive/Desktop/Post-Harvest-DBMS/docs/project/PROJECT_CONTEXT.md): System context, operational background, and boundaries.
  - [SCOPE_AND_OBJECTIVES.md](file:///c:/Users/raksh/OneDrive/Desktop/Post-Harvest-DBMS/docs/project/SCOPE_AND_OBJECTIVES.md): Project goals, deliverables, and out-of-scope boundaries.
  - [REQUIREMENTS.md](file:///c:/Users/raksh/OneDrive/Desktop/Post-Harvest-DBMS/docs/project/REQUIREMENTS.md): Functional and non-functional specifications.
  - [DASHBOARD_SPECIFICATION.md](file:///c:/Users/raksh/OneDrive/Desktop/Post-Harvest-DBMS/docs/project/DASHBOARD_SPECIFICATION.md): UI pages, layout, and component specifications.
- **Architecture & Technology**:
  - [SYSTEM_ARCHITECTURE.md](file:///c:/Users/raksh/OneDrive/Desktop/Post-Harvest-DBMS/docs/architecture/SYSTEM_ARCHITECTURE.md): Multi-tier architecture and data flows.
  - [TECH_STACK.md](file:///c:/Users/raksh/OneDrive/Desktop/Post-Harvest-DBMS/docs/architecture/TECH_STACK.md): Pinned stack, environment compatibility, and justification.
  - [ARCHITECTURE_AUDIT.md](file:///c:/Users/raksh/OneDrive/Desktop/Post-Harvest-DBMS/docs/architecture/ARCHITECTURE_AUDIT.md): Detailed audit of source diagrams and discrepancies.
- **Database & Data Modeling**:
  - [DIAGRAM_INVENTORY.md](file:///c:/Users/raksh/OneDrive/Desktop/Post-Harvest-DBMS/docs/diagrams/DIAGRAM_INVENTORY.md): Source diagram inventory and checksums.
  - [ER_TO_RELATIONAL_MAPPING.md](file:///c:/Users/raksh/OneDrive/Desktop/Post-Harvest-DBMS/docs/database/ER_TO_RELATIONAL_MAPPING.md): Detailed entity and relationship mapping.
  - [DATA_OWNERSHIP_MATRIX.md](file:///c:/Users/raksh/OneDrive/Desktop/Post-Harvest-DBMS/docs/database/DATA_OWNERSHIP_MATRIX.md): SQL vs NoSQL store allocation matrix.
  - [MYSQL_DESIGN.md](file:///c:/Users/raksh/OneDrive/Desktop/Post-Harvest-DBMS/docs/database/MYSQL_DESIGN.md): Relational tables, indexes, constraints, and audit log.
  - [MONGODB_DESIGN.md](file:///c:/Users/raksh/OneDrive/Desktop/Post-Harvest-DBMS/docs/database/MONGODB_DESIGN.md): Document collections, JSON schemas, and indexing.
- **Interfaces & Operations**:
  - [API_CONTRACT.md](file:///c:/Users/raksh/OneDrive/Desktop/Post-Harvest-DBMS/docs/api/API_CONTRACT.md): FastAPI REST endpoints, schemas, and error responses.
  - [SIMULATION_SPEC.md](file:///c:/Users/raksh/OneDrive/Desktop/Post-Harvest-DBMS/docs/simulation/SIMULATION_SPEC.md): Deterministic generator logic, states, and scenarios.
  - [DECISION_LOG.md](file:///c:/Users/raksh/OneDrive/Desktop/Post-Harvest-DBMS/docs/decisions/DECISION_LOG.md): Architectural and schema decisions log.
  - [TEAM_RESPONSIBILITIES.md](file:///c:/Users/raksh/OneDrive/Desktop/Post-Harvest-DBMS/docs/team/TEAM_RESPONSIBILITIES.md): Role boundaries and collaboration workflow.

---

## 5. Local Setup & Quickstart

See [TECH_STACK.md](file:///c:/Users/raksh/OneDrive/Desktop/Post-Harvest-DBMS/docs/architecture/TECH_STACK.md) for full environmental prerequisite instructions.

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

# Install backend dependencies (when finalized)
pip install -r backend/requirements.txt

# Install frontend dependencies (when finalized)
cd frontend
npm install
cd ..
```

---

## 6. Contributing
All code changes must be submitted via pull request on a dedicated feature branch. See [CONTRIBUTING.md](file:///c:/Users/raksh/OneDrive/Desktop/Post-Harvest-DBMS/CONTRIBUTING.md) for rules and branch naming conventions.

