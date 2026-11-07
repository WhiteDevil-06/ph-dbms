---
name: backend-fastapi
description: Develop FastAPI endpoints, Pydantic schemas, SQLAlchemy models, and PyMongo repositories following modular monolith patterns.
---

# FastAPI Backend Skill

Use this skill when developing or debugging backend routes, data ingestion services, repository queries, and API response models.

## Architecture Guidelines
1. **Layer Separation**:
   - `api/`: Route definitions and dependency injection.
   - `schemas/`: Pydantic request and response models.
   - `services/`: Business validation and cross-repository transactions.
   - `repositories/`: Direct database queries for MySQL and MongoDB.
   - `models/`: SQLAlchemy ORM definitions.
2. **API Contract Adherence**: Always verify schemas against `docs/api/API_CONTRACT.md`.
3. **Primary References**:
   - [API_CONTRACT.md](file:///c:/Users/raksh/OneDrive/Desktop/Post-Harvest-DBMS/docs/api/API_CONTRACT.md)
   - [SYSTEM_ARCHITECTURE.md](file:///c:/Users/raksh/OneDrive/Desktop/Post-Harvest-DBMS/docs/architecture/SYSTEM_ARCHITECTURE.md)
   - [backend/README.md](file:///c:/Users/raksh/OneDrive/Desktop/Post-Harvest-DBMS/backend/README.md)

