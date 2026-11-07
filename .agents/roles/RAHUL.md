# Role Brief: Backend and Database Integration Developer
**Owner**: Rahul

---

## 1. Role Title and Owner
- **Role Title**: Backend & Database Integration Developer
- **Owner**: Rahul

---

## 2. Project Context
This project, titled **"Intelligent Data Management and Operational Analytics for Autonomous Post-Harvest Material Handling Systems"**, provides the data management, persistence, monitoring, and operational analytics layer for an autonomous post-harvest agricultural robotics system. Because physical robotics hardware is actively under construction, there is no live robot integration in this phase. Rahul is responsible for implementing the FastAPI application, service/repository abstractions, database integrations (MySQL 8.4 via SQLAlchemy and MongoDB 8.0 via PyMongo), the deterministic simulated data generator, and clean REST APIs consumed by Ramcharan's frontend dashboard.

---

## 3. Ownership and Explicit Non-Ownership
- **Owns**:
  - Python backend application architecture using FastAPI and Pydantic.
  - Integration with MySQL 8.4 LTS (structured operational records) and MongoDB 8.0 (detections, inference metadata, telemetry logs) according to the approved data ownership matrix.
  - Strict input validation, error handling, and business service logic.
  - Seeded, deterministic simulation data generator (`simulator/`).
  - OpenAPI specification and maintenance of `docs/api/API_CONTRACT.md`.
  - Backend automated unit and integration tests (`backend/tests/`).
  - Backend setup guide and testing documentation in `backend/README.md`.
- **Explicit Non-Ownership & Strict Prohibitions**:
  - Must **never** silently redefine the ER model, relational schema, or data ownership boundaries without Rakshith's approval.
  - Must **never** expose database credentials or direct database access to frontend code.
  - Must **never** describe simulated data inputs as live robot telemetry or genuine physical operations.
  - Must **never** alter API endpoint paths, query parameters, or payload contracts without notifying Ramcharan and updating `docs/api/API_CONTRACT.md`.

---

## 4. Step-by-Step Responsibilities
1. Review the architecture audit in `docs/architecture/ARCHITECTURE_AUDIT.md` and data ownership matrix in `docs/database/DATA_OWNERSHIP_MATRIX.md`.
2. Implement backend structure: `core/`, `api/`, `models/`, `schemas/`, `services/`, and `repositories/`.
3. Set up database connectivity: SQLAlchemy engine/sessionmaker for MySQL and PyMongo client for MongoDB.
4. Implement Pydantic schemas enforcing strict validation and simulation provenance defaults (`SIMULATED`).
5. Develop repository classes isolating raw SQL / PyMongo operations.
6. Implement the deterministic simulation generator supporting configurable seed, scale, and safe data reseeding.
7. Implement FastAPI routers matching `docs/api/API_CONTRACT.md`.
8. Write comprehensive unit and integration tests using `pytest`.

---

## 5. Files and Folders to Read First
1. `AGENTS.md`
2. `docs/project/PROJECT_CONTEXT.md`
3. `docs/architecture/ARCHITECTURE_AUDIT.md`
4. `docs/architecture/TECH_STACK.md`
5. `docs/database/DATA_OWNERSHIP_MATRIX.md`
6. `docs/database/MYSQL_DESIGN.md`
7. `docs/database/MONGODB_DESIGN.md`
8. `docs/api/API_CONTRACT.md`
9. `docs/simulation/SIMULATION_SPEC.md`
10. `backend/README.md`
11. `.agents/roles/RAHUL.md`

---

## 6. Files and Folders to Create or Maintain
- `backend/app/**/*`
- `backend/tests/**/*`
- `backend/requirements.txt`
- `backend/README.md`
- `simulator/**/*`
- `docs/api/API_CONTRACT.md`
- `docs/simulation/SIMULATION_SPEC.md`

---

## 7. Interfaces and Dependencies with Other Members
- **With Rakshith Raghavendra (Project Lead & Database Architect)**:
  - Receives finalized MySQL DDL and migrations; aligns SQLAlchemy ORM models with them.
  - Adheres to the approved data ownership matrix for SQL vs NoSQL document routing.
- **With Ramcharan (Frontend Developer)**:
  - Provides reliable, versioned FastAPI REST endpoints.
  - Ensures OpenAPI docs at `/docs` are always synchronized with `docs/api/API_CONTRACT.md`.
  - Coordinates CORS policies and local development ports.

---

## 8. Branch and Pull Request Expectations
- Work branch: `feature/rahul-backend` or `feature/api-<endpoint>`.
- Never push directly to `main`.
- Pull Requests must include a clear explanation of business logic, database queries, and test execution results (`pytest` run commands and terminal outputs).

---

## 9. Definition of Done and Testing Expectations
- Code passes linting (`flake8` / `black --check`).
- All tests pass via `pytest backend/tests/` with zero failures.
- Endpoints return appropriate HTTP status codes (200, 201, 400, 404, 422).
- All inserted simulation records carry `provenance = "SIMULATED"`.
- Database connections handle timeouts and failures gracefully without leaking sensitive connection details.

---

## 10. Copyable Prompt for Rahul to Give His IDE Agent
```text
I am Rahul, Backend and Database Integration Developer for the Post-Harvest DBMS project.
Please read:
1. AGENTS.md
2. docs/project/PROJECT_CONTEXT.md
3. docs/architecture/ARCHITECTURE_AUDIT.md
4. docs/architecture/TECH_STACK.md
5. docs/database/DATA_OWNERSHIP_MATRIX.md
6. docs/database/MYSQL_DESIGN.md
7. docs/database/MONGODB_DESIGN.md
8. docs/api/API_CONTRACT.md
9. docs/simulation/SIMULATION_SPEC.md
10. .agents/roles/RAHUL.md
11. backend/README.md

Act strictly within my role as Backend Developer. Help me implement the FastAPI backend, SQLAlchemy and PyMongo repositories, simulation data generator, and API endpoints adhering to the API contract and data ownership matrix. Do not modify the relational schema without Rakshith's approval, and do not write frontend code.
```

