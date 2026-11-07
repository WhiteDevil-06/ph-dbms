# AGENTS.md — Global Multi-Agent Engineering Instructions

## 1. Project Identity and Context
- **Project Title**: Intelligent Data Management and Operational Analytics for Autonomous Post-Harvest Material Handling Systems
- **Repository Scope**: Post-harvest material handling DBMS, data persistence, monitoring, and operational analytics layer.
- **Physical Boundary**: This repository is **not** the robot's command-and-control system. Motor control, navigation control, manipulator actuation, and safety-critical robot execution are handled by an external robotics system.
- **Phase Status**: The physical robot is under construction. All data in this phase is generated via a deterministic, seeded simulator. Live robot integration is out of scope. Never label simulated records as real physical operations or live telemetry.

---

## 2. Mandatory Reading Order
Before proposing edits, creating schemas, or writing application code, every agent (human or AI) must read project files in the following strict order:
1. `AGENTS.md` (this file)
2. `docs/project/PROJECT_CONTEXT.md`
3. `docs/architecture/ARCHITECTURE_AUDIT.md`
4. `docs/architecture/TECH_STACK.md`
5. Relevant role brief in `.agents/roles/<ROLE>.md`:
   - `RAKSHITH_RAGHAVENDRA.md` (Project Lead & Database Architect)
   - `RAMCHARAN.md` (Frontend & Dashboard Developer)
   - `RAHUL.md` (Backend & Database Integration Developer)
6. Relevant module README and contracts:
   - `docs/database/DATA_OWNERSHIP_MATRIX.md`
   - `docs/database/ER_TO_RELATIONAL_MAPPING.md`
   - `docs/api/API_CONTRACT.md`
   - `docs/simulation/SIMULATION_SPEC.md`
   - Relevant `README.md` (`backend/`, `frontend/`, `simulator/`, `database/`)
7. Applicable `.agent/rules/` and `.agent/workflows/`.

---

## 3. Epistemic Classification and Truth Discipline
To avoid hallucination and unapproved divergence, every statement, proposal, or schema element must be explicitly categorized:
- **SOURCE FACT**: Explicitly depicted in original source diagrams (`docs/diagrams/`) or explicit user instructions.
- **TEAM DECISION**: Formally confirmed by the project lead / team and logged in `docs/decisions/DECISION_LOG.md`.
- **PROPOSAL**: Recommended architecture or implementation pattern requiring team review and sign-off before adoption.
- **UNKNOWN**: Missing, conflicting, or unverified information that must be resolved prior to implementation.

---

## 4. Mandatory Behavioral Rules
1. **Never Fabricate**: Do not invent table columns, foreign keys, relationships, API routes, response fields, robot states, telemetry data, or test passes.
2. **Never Claim False Verification**: Never claim a test passed unless the test command was executed and exited with code 0. Never claim a database is connected unless a connection handshake was executed and verified.
3. **Respect Provenance**: All generated, seeded, or manual data must carry an explicit provenance tag (`SIMULATED` or `MANUAL_TEST`). Dashboards must display a persistent "SIMULATION DATA" indicator.
4. **Data Safety**: Never drop databases, truncate tables, delete collections, overwrite files, or execute destructive commands without explicit written confirmation. Explain all migration risks beforehand.
5. **Role Discipline**: Respect module ownership:
   - Rakshith Raghavendra owns relational schema, core architecture, and final integration.
   - Ramcharan owns the React/TypeScript dashboard and consumes documented API contracts only.
   - Rahul owns the FastAPI backend, service/repository layers, database drivers, and simulator ingestion.
6. **No Direct Secret Commits**: Never commit `.env`, credentials, local database dumps, or passwords.
7. **Git Safety**: Never push directly to `main`. Never force-push. Never commit or push to remote repositories on behalf of the user unless specifically instructed.

---

## 5. Directory & File Reference Links
- Context: [PROJECT_CONTEXT.md](file:///c:/Users/raksh/OneDrive/Desktop/Post-Harvest-DBMS/docs/project/PROJECT_CONTEXT.md)
- Audit: [ARCHITECTURE_AUDIT.md](file:///c:/Users/raksh/OneDrive/Desktop/Post-Harvest-DBMS/docs/architecture/ARCHITECTURE_AUDIT.md)
- Tech Stack: [TECH_STACK.md](file:///c:/Users/raksh/OneDrive/Desktop/Post-Harvest-DBMS/docs/architecture/TECH_STACK.md)
- Decision Log: [DECISION_LOG.md](file:///c:/Users/raksh/OneDrive/Desktop/Post-Harvest-DBMS/docs/decisions/DECISION_LOG.md)
- API Contract: [API_CONTRACT.md](file:///c:/Users/raksh/OneDrive/Desktop/Post-Harvest-DBMS/docs/api/API_CONTRACT.md)
- Contributing: [CONTRIBUTING.md](file:///c:/Users/raksh/OneDrive/Desktop/Post-Harvest-DBMS/CONTRIBUTING.md)

