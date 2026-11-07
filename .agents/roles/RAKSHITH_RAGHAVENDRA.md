# Role Brief: Project Lead and Database Architect
**Owner**: Rakshith Raghavendra

---

## 1. Role Title and Owner
- **Role Title**: Project Lead & Database Architect
- **Owner**: Rakshith Raghavendra

---

## 2. Project Context
This project, titled **"Intelligent Data Management and Operational Analytics for Autonomous Post-Harvest Material Handling Systems"**, provides the data management, persistence, monitoring, and operational analytics layer for an autonomous post-harvest agricultural robotics system. The external robotics platform is currently under active construction, meaning all data in this phase is generated using an internal, seeded simulator. Live robot integration is strictly out of scope. The DBMS must reliably capture, index, and query operational sessions, tasks, decisions, operations, detections, devices, and system events without acting as a real-time robot controller.

---

## 3. Ownership and Explicit Non-Ownership
- **Owns**:
  - Overall repository foundation, Git workflow, milestones, and project coordination.
  - Scope boundaries, architectural integrity, and the project decision log (`docs/decisions/DECISION_LOG.md`).
  - Review and finalization of ER model, DFDs, relational schema, and the SQL–NoSQL data ownership matrix.
  - MySQL 8.4 LTS relational database design: schema definitions, table DDL, keys, indexes, constraints, migrations, and seed scripts.
  - Data contracts with Rahul and API expectations with Ramcharan.
  - Cross-module integration review, PR approvals, code quality assurance, and final project acceptance.
- **Explicit Non-Ownership**:
  - Does **not** write all backend service and endpoint implementation code (owned by Rahul).
  - Does **not** write frontend React components, layouts, or CSS (owned by Ramcharan).
  - Does **not** act as the sole implementer, sole debugger, and sole documenter of the entire codebase.

---

## 4. Step-by-Step Responsibilities
1. Audit and resolve diagram discrepancies recorded in `docs/architecture/ARCHITECTURE_AUDIT.md`.
2. Finalize the ER-to-Relational mapping and the SQL vs NoSQL store allocation in `docs/database/DATA_OWNERSHIP_MATRIX.md`.
3. Author production-grade MySQL 8.4 DDL in `database/mysql/schema/` and versioned migration scripts in `database/mysql/migrations/`.
4. Ensure primary keys, foreign key constraints (resolving the `TASK.task_id` self-reference issue), and indexes are correctly defined.
5. Review and sign off on API contracts (`docs/api/API_CONTRACT.md`) drafted by Rahul and consumed by Ramcharan.
6. Conduct peer reviews of Pull Requests submitted by Rahul and Ramcharan.
7. Manage Git releases and maintain clean Git history on `main`.

---

## 5. Files and Folders to Read First
1. `AGENTS.md`
2. `docs/project/PROJECT_CONTEXT.md`
3. `docs/architecture/ARCHITECTURE_AUDIT.md`
4. `docs/diagrams/DIAGRAM_INVENTORY.md`
5. `docs/database/ER_TO_RELATIONAL_MAPPING.md`
6. `docs/database/DATA_OWNERSHIP_MATRIX.md`
7. `docs/database/MYSQL_DESIGN.md`
8. `docs/decisions/DECISION_LOG.md`
9. `CONTRIBUTING.md`

---

## 6. Files and Folders to Create or Maintain
- `database/mysql/schema/*.sql`
- `database/mysql/migrations/*.sql`
- `database/mysql/seed/*.sql`
- `docs/database/ER_TO_RELATIONAL_MAPPING.md`
- `docs/database/DATA_OWNERSHIP_MATRIX.md`
- `docs/database/MYSQL_DESIGN.md`
- `docs/decisions/DECISION_LOG.md`
- `docs/architecture/ARCHITECTURE_AUDIT.md`
- `docker-compose.yml`

---

## 7. Interfaces and Dependencies with Other Members
- **With Rahul (Backend Developer)**:
  - Supplies the approved MySQL schema and migration scripts.
  - Reviews Rahul's SQLAlchemy ORM models (`backend/app/models/`) to ensure exact alignment with DDL.
  - Confirms the relational vs document data boundary.
- **With Ramcharan (Frontend Developer)**:
  - Approves high-level analytics query requirements and dashboard reporting metrics.
  - Ensures relational tables capture the required analytical dimensions (e.g. durations, outcome status).

---

## 8. Branch and Pull Request Expectations
- Work branch: `feature/database-foundation` or `feature/schema-<topic>`.
- Never push directly to `main`.
- Pull Requests must detail schema changes, explain foreign key constraints and indexing strategies, and provide verification that migrations execute cleanly without data loss.

---

## 9. Definition of Done and Testing Expectations
- MySQL DDL executes without syntax errors on MySQL 8.4 LTS.
- Foreign key constraints enforce referential integrity and prevent orphan records.
- Primary keys are non-null and uniquely indexed.
- Discrepancies identified in the audit (such as `rescription` typo and `TASK.task_id` self-reference) are corrected in DDL.
- All schema decisions are documented in `docs/decisions/DECISION_LOG.md`.

---

## 10. Copyable Prompt for Rakshith to Give His IDE Agent
```text
I am Rakshith Raghavendra, Project Lead and Database Architect for the Post-Harvest DBMS project.
Please read:
1. AGENTS.md
2. docs/project/PROJECT_CONTEXT.md
3. docs/architecture/ARCHITECTURE_AUDIT.md
4. docs/architecture/TECH_STACK.md
5. .agents/roles/RAKSHITH_RAGHAVENDRA.md
6. docs/database/ER_TO_RELATIONAL_MAPPING.md
7. docs/database/DATA_OWNERSHIP_MATRIX.md
8. docs/decisions/DECISION_LOG.md

Act strictly within my role as Database Architect and Project Lead. Help me resolve architecture audit items, finalize the relational MySQL schema and migrations, maintain the decision log, and coordinate integration with Rahul and Ramcharan. Do not implement backend API routes or frontend UI components.
```

