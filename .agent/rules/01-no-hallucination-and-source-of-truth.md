# Rule 01: Truth Discipline and Anti-Hallucination

## Epistemic Integrity
Agents must strictly ground every statement and code artifact in verified repository facts:
- **SOURCE FACT**: Documented directly in original diagram images (`docs/diagrams/`) or explicit instructions.
- **TEAM DECISION**: Decided by team consensus, approved by the Project Lead, and logged in `docs/decisions/DECISION_LOG.md`.
- **PROPOSAL**: An engineering recommendation undergoing review; never treated as an established requirement.
- **UNKNOWN**: Ambiguities or missing details that require clarification before code or migrations are created.

## Hard Prohibitions
1. Never invent database columns, foreign keys, relationships, or tables that are not verified.
2. Never invent API endpoints, query parameters, or payload fields.
3. Never claim unit or integration tests passed without executing the test commands and reporting results.
4. Never claim databases are running or connected without active verification.
5. Never assume inter-frame object tracking exists; a `detection_id` is an independent spatial observation unless persistent object tracking is explicitly approved.

