# Rule 03: Coding and Quality Standards

## General Principles
- Maintain clean, readable, modular code adhering to PEP 8 for Python and standard TypeScript/ESLint guidelines.
- Preserve existing comments and docstrings unless explicitly asked to modify them.
- All code must run and pass tests in the local Windows 11 environment.

## Backend Standards (Rahul)
- Maintain strict separation of concerns:
  - `app/api/`: Routing, parameter validation, and HTTP responses.
  - `app/schemas/`: Pydantic request and response models.
  - `app/services/`: Business logic, transaction orchestration, and cross-model workflows.
  - `app/repositories/`: Direct database queries and data persistence.
  - `app/models/`: SQLAlchemy ORM models.
- Parameterize all database queries. Avoid raw SQL string interpolation.
- Validate all incoming payloads with Pydantic schemas.

## Frontend Standards (Ramcharan)
- Use functional React components with TypeScript interfaces.
- Separate view presentation (`components/`, `pages/`) from data fetching (`hooks/`, `api/`).
- Provide explicit UI states for:
  - Loading states (skeletons or spinners)
  - Empty states (informative empty placeholders)
  - Error states (user-friendly alerts without backend stack traces)
  - Simulation state (persistent badge/banner)
- Do not hardcode API URLs; use `import.meta.env.VITE_API_BASE_URL`.

## Database Standards (Rakshith)
- Name tables in lower_snake_case (plural or singular per project standard; singular chosen in source diagrams).
- All primary keys must be explicitly typed (`VARCHAR(36)` UUID or `BIGINT AUTO_INCREMENT`).
- Foreign keys must be indexed and enforce explicit referential integrity (`ON DELETE RESTRICT` or `CASCADE` where justified).
- Never execute unreviewed migrations or destructive DDL commands (`DROP`, `TRUNCATE`).

