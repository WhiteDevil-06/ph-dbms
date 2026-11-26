# PH-DBMS Operations Dashboard

Responsive React dashboard for the post-harvest DBMS. The browser communicates
only with the FastAPI gateway; it never connects directly to MySQL or MongoDB.
All displayed operational data is clearly identified as simulated.

## Technology

- React 18 and TypeScript
- Vite and Tailwind CSS
- React Router DOM
- Axios
- TanStack Query
- Recharts and Lucide React

## Setup

Requirements: Node.js 20+ and npm 10+.

From the repository root, start the backend using the project's documented
setup, then run:

```powershell
cd frontend
npm install
npm run dev
```

The Vite server runs at `http://localhost:5173`. Its development proxy forwards
`/api` and `/health` to `http://localhost:8000`.

## Commands

```powershell
npm run dev
npm run typecheck
npm run lint
npm run build
npm run preview
```

`npm run build` runs the TypeScript project build before Vite bundles the app.

## API configuration and integration

The Axios client uses relative URLs by default. To direct requests to another
FastAPI origin, define `VITE_API_BASE_URL` in the frontend environment. Never
put credentials or database connection strings in frontend environment files.

Implemented by the backend and integrated by this frontend:

| Method | Path | Frontend behavior |
| --- | --- | --- |
| `GET` | `/health` | Backend connectivity indicator, refreshed every 30 seconds |
| `GET` | `/api/v1/simulation/status` | Dataset counts, mode, and seed; refreshed and invalidated after mutations |
| `POST` | `/api/v1/simulation/generate` | Seed/scale/reset-first form with mutation feedback |
| `POST` | `/api/v1/simulation/reset` | Explicit confirmation dialog; targets `SIMULATED_ONLY` |

The following documented routes were **not implemented** in the inspected
backend and are not requested by this frontend. Their views communicate pending
integration and do not display fabricated records:

- Sessions: `GET /api/v1/sessions`, `GET /api/v1/sessions/{session_id}`
- Tasks: `GET /api/v1/tasks`, `GET /api/v1/tasks/{task_id}`
- Detections: `GET /api/v1/detections`, `GET /api/v1/detections/{detection_id}`
- Operations: `GET /api/v1/operations`
- Decisions: `GET /api/v1/decisions`
- System events: `GET /api/v1/system-events`, `PATCH /api/v1/system-events/{event_id}`
- Analytics: `GET /api/v1/analytics/overview`, `/produce-classes`, `/operation-outcomes`
- Equipment and models: `GET /api/v1/devices`, `GET /api/v1/models`

The backend implementation was checked in `backend/app/main.py`; endpoint
availability can change independently of this frontend.

## Pages

1. Overview / simulation status
2. Sessions
3. Tasks
4. Detections
5. Operations
6. Decisions
7. System events
8. Analytics
9. Equipment & models

The Overview uses real health and simulation responses. All eight other views
have their page-specific table, filter, chart, drawer/modal, or registry
layouts ready for data. Until their corresponding backend routes exist, they
show an explicit API-unavailable state, empty records, and disabled data-bound
controls; they never show fabricated operational records. CSV export remains
disabled pending approval. The persistent simulation banner and detections
tracking notice are shown regardless of route.

## Structure

```text
src/
├── api/          # Axios client and FastAPI service functions
├── components/   # Shared UI and simulation controls
├── hooks/        # TanStack Query hooks
├── layouts/      # Responsive dashboard shell
├── pages/        # Overview and module integration-status pages
├── styles/       # Global styles and Tailwind entrypoint
└── types/        # Verified health and simulation response contracts
```
