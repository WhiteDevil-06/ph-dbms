# Team Responsibilities and Collaboration Governance

## 1. Team Directory and Core Ownership

| Member | Academic Role | Primary Responsibilities | Strict Non-Responsibilities |
| :--- | :--- | :--- | :--- |
| **Rakshith Raghavendra** | Project Lead & Database Architect | Scope, architecture decisions, ER/relational models, MySQL 8.4 schema & migrations, decision log, final acceptance | Does not implement entire backend API or frontend React code. |
| **Ramcharan** | Frontend & Dashboard Developer | React 18 / TypeScript frontend, Vite build, Tailwind CSS layout, Recharts analytics, API consumption, simulation banner | Never touches MySQL/MongoDB directly; never invents undocumented API endpoints. |
| **Rahul** | Backend & Database Integration Developer | FastAPI application, Pydantic schemas, SQLAlchemy & PyMongo repositories, simulation data generator, API contract | Never redefines database schemas unilaterally; never describes simulated data as live robot data. |

---

## 2. Code Ownership and Review Matrix

| Repository Subdirectory | Primary Owner | Mandatory Reviewer |
| :--- | :--- | :--- |
| `database/mysql/` | Rakshith Raghavendra | Rahul |
| `database/mongodb/` | Rahul / Rakshith | Rakshith Raghavendra |
| `backend/app/` | Rahul | Rakshith Raghavendra / Ramcharan |
| `backend/tests/` | Rahul | Rakshith Raghavendra |
| `frontend/src/` | Ramcharan | Rahul / Rakshith Raghavendra |
| `simulator/` | Rahul | Rakshith Raghavendra |
| `docs/api/` | Rahul & Ramcharan (Joint) | Rakshith Raghavendra |
| `docs/decisions/` | Rakshith Raghavendra | Rahul & Ramcharan |

---

## 3. Communication & Interface Synchronization Rules

1. **Schema Changes**: Rakshith must announce schema modifications and log them in `docs/decisions/DECISION_LOG.md` before Rahul modifies SQLAlchemy models.
2. **API Contract Changes**: If Rahul needs to adjust request/response formats or endpoint paths, he must update `docs/api/API_CONTRACT.md` and notify Ramcharan before merging.
3. **Frontend Requests**: If Ramcharan needs additional fields or aggregate metrics for a UI chart, he opens a proposal issue and discusses it with Rahul and Rakshith before assuming the field exists.
4. **Peer Review Invariant**: No Pull Request may be merged without at least one teammate review approval.

