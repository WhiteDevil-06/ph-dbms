# Rule 02: Architecture and Data Boundaries

## System Separation
The system is implemented as a modular monolith:
1. **Frontend**: React + TypeScript + Vite + Tailwind CSS dashboard.
2. **Backend**: FastAPI + Pydantic + SQLAlchemy + PyMongo.
3. **Relational Database**: MySQL 8.4 LTS for structured relational operational records.
4. **Document Database**: MongoDB Community Server 8.0 for semi-structured inference data and telemetry logs.

## Boundary Invariants
1. **Frontend Isolation**: The browser client communicates strictly with FastAPI via HTTP/JSON. The frontend must **never** connect directly to MySQL or MongoDB. No database connection strings, credentials, or ORM objects may exist in client code.
2. **Database Division of Authority**:
   - MySQL is authoritative for `sessions`, `tasks`, `operations`, `decisions`, and `devices`.
   - MongoDB is authoritative for `detections`, model configurations, and high-frequency/detailed telemetry events.
   - Dual-writing or duplicate authoritative records across both databases without a documented consistency strategy is prohibited.
3. **No Unapproved Infrastructure**:
   - No microservices, Kafka, Redis, Kubernetes, or cloud services may be introduced without project-lead approval.

