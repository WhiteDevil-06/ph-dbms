# Workflow: Implement Database Change

## Owner
Rakshith Raghavendra (Project Lead and Database Architect)

## Steps
1. **Analyze Schema Impact**:
   - Check proposed change against `docs/database/ER_TO_RELATIONAL_MAPPING.md` and `docs/database/DATA_OWNERSHIP_MATRIX.md`.
   - Identify whether the change affects MySQL (relational) or MongoDB (document).
2. **Draft Decision Record**:
   - Log rationale, alternatives considered, and risks in `docs/decisions/DECISION_LOG.md`.
   - Obtain confirmation from team before modifying schema scripts.
3. **Draft Migration / Schema Script**:
   - For MySQL: Create forward-only SQL migration in `database/mysql/migrations/` (or update baseline schema in `database/mysql/schema/`).
   - For MongoDB: Update collection validator or index definitions in `database/mongodb/`.
4. **Update ORM / Schema Models**:
   - Coordinate with Rahul to update SQLAlchemy models in `backend/app/models/` and Pydantic schemas in `backend/app/schemas/`.
5. **Run Verification**:
   - Apply migration against local test database.
   - Verify foreign key constraints, indexes, and default values.
   - Confirm zero regression on existing seed queries.

