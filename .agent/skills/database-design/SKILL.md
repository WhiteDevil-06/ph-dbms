---
name: database-design
description: Design, audit, and modify MySQL 8.4 relational schemas and MongoDB 8.0 document collections in accordance with approved diagrams and data ownership.
---

# Database Design Skill

Use this skill when auditing or drafting schemas, migrations, table definitions, foreign key constraints, or MongoDB collection structures.

## Critical Invariants
1. **Never Invent Columns**: All columns must map to approved entities in `docs/database/ER_TO_RELATIONAL_MAPPING.md`.
2. **Consult Data Ownership**: Verify whether data belongs in MySQL or MongoDB using `docs/database/DATA_OWNERSHIP_MATRIX.md`.
3. **Discrepancy Awareness**:
   - Do not implement the accidental `TASK.task_id` self-reference.
   - Use `rationale` instead of the typo `rescription`.
   - Ensure `session_id` is an explicit foreign key on `task`.
4. **Primary References**:
   - [MYSQL_DESIGN.md](file:///c:/Users/raksh/OneDrive/Desktop/Post-Harvest-DBMS/docs/database/MYSQL_DESIGN.md)
   - [MONGODB_DESIGN.md](file:///c:/Users/raksh/OneDrive/Desktop/Post-Harvest-DBMS/docs/database/MONGODB_DESIGN.md)
   - [ARCHITECTURE_AUDIT.md](file:///c:/Users/raksh/OneDrive/Desktop/Post-Harvest-DBMS/docs/architecture/ARCHITECTURE_AUDIT.md)

