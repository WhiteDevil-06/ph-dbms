# Workflow: Audit Project Context

## Purpose
Inspect repository documents, diagram sources, and environment configurations before starting any major architectural, schema, or implementation task.

## Steps
1. **Read Core Files**:
   - Check `AGENTS.md` and `docs/project/PROJECT_CONTEXT.md`.
   - Read `docs/architecture/ARCHITECTURE_AUDIT.md` for known discrepancies.
2. **Verify Diagrams**:
   - Check that `docs/diagrams/` images match `docs/diagrams/DIAGRAM_INVENTORY.md`.
3. **Verify Decision Log**:
   - Read `docs/decisions/DECISION_LOG.md` to identify approved decisions vs unapproved proposals.
4. **Inspect Tooling**:
   - Confirm active Python virtual environment and Node.js versions.
   - Verify local database ports (MySQL 3306, MongoDB 27017).
5. **Classify Uncertainty**:
   - Explicitly label all assumptions as SOURCE FACT, TEAM DECISION, PROPOSAL, or UNKNOWN.

