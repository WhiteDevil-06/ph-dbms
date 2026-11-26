# API Contract Specification (FastAPI REST Gateway)
**Owners**: Rahul (Backend Developer) & Ramcharan (Frontend Developer)

---

## 1. Gateway Principles
- **Base URL Prefix**: `/api/v1`
- **Format**: All requests and responses use `application/json; charset=utf-8`.
- **CORS Allowed Origins**: Configured in `.env` (default `http://localhost:5173`, `http://127.0.0.1:5173`).
- **Authentication & RBAC (DEC-08)**: All `/api/v1/*` operational endpoints (except `POST /api/v1/auth/login`) require `Authorization: Bearer <jwt>` signed with `HS256` (8-hour TTL). Two roles are enforced server-side: `ADMIN` and `OPERATOR`.
- **Data Provenance**: Every response object containing operational or simulated telemetry includes a `provenance` field (`"SIMULATED"` or `"MANUAL_TEST"`).

---

## 2. Standard Response Headers & Error Schemas

### Standard Error Response (HTTP 4xx / 5xx)
```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "Task with ID 'tsk-12345' was not found.",
    "details": null,
    "timestamp": "2026-11-04T12:00:00Z"
  }
}
```

---

## 3. Endpoints Register

### 3.1 System Health and Status
- **`GET /health`**
  - **Description**: Returns actual real-time connectivity status of backend services and databases. Never returns fabricated "OK" status if databases are unreachable.
  - **Response 200 OK**:
    ```json
    {
      "status": "healthy",
      "timestamp": "2026-11-04T12:00:00Z",
      "version": "1.0.0",
      "data_source_mode": "SIMULATION",
      "services": {
        "mysql": "connected",
        "mongodb": "connected"
      }
    }
    ```

### 3.1A Authentication, JWT Sessions & RBAC (`/api/v1/auth`)
- **`POST /api/v1/auth/login`** (Public; brute-force rate-limited → `429`)
  - **Request Body**: `{ "username": "admin", "password": "<password>" }`
  - **Response 200 OK**: `{ "access_token", "token_type": "bearer", "expires_in": 28800, "expires_at", "user": { "user_id", "username", "full_name", "role", "is_active", "permissions", "provenance", "created_at" } }`
  - **Errors**: `401 Unauthorized` (generic `"Invalid username or password."`), `422 Unprocessable Entity`, `429 Too Many Requests`.
- **`POST /api/v1/auth/logout`** (`ADMIN` & `OPERATOR`)
  - **Description**: Revokes the caller's JWT `jti` server-side in MySQL `revoked_token` and records a `LOGOUT` audit event. Subsequent replays of the revoked token return `401 Unauthorized`.
- **`GET /api/v1/auth/me`** (`ADMIN` & `OPERATOR`)
  - **Description**: Returns the authenticated principal, role, granted permissions, `jti`, and `expires_at`.
- **`GET /api/v1/auth/permissions-matrix`** (`ADMIN` & `OPERATOR`)
  - **Description**: Returns the authoritative RBAC role differentiation matrix for `ADMIN` vs `OPERATOR`.
- **`GET /api/v1/auth/users`** (`ADMIN` only; `403` for `OPERATOR`)
  - **Description**: Returns registered accounts without `password_hash`.
- **`GET /api/v1/auth/audit-logs`** (`ADMIN` only; `403` for `OPERATOR`)
  - **Query Params**: `limit` (1–200, default 50).
  - **Description**: Returns recent `LOGIN_SUCCESS`, `LOGIN_FAILED`, `LOGOUT`, `ACCESS_DENIED`, and `RATE_LIMITED` records.

### 3.2 Simulation Engine Management (JWT Protected)
- **RBAC Rules**:
  - `GET /api/v1/simulation/status`: `ADMIN` & `OPERATOR` (`401` if unauthenticated)
  - `POST /api/v1/simulation/generate`: `ADMIN` (full), `OPERATOR` (`reset_first=false` only; `reset_first=true` returns `403 Forbidden`)
  - `POST /api/v1/simulation/reset`: `ADMIN` only (`403 Forbidden` for `OPERATOR`)
- **`GET /api/v1/simulation/status`**
  - **Description**: Returns current simulation configuration, active seed, and generated record totals.
  - **Response 200 OK**:
    ```json
    {
      "mode": "SIMULATED",
      "active_seed": 42,
      "counts": {
        "sessions": 10,
        "tasks": 60,
        "operations": 120,
        "detections": 350,
        "decisions": 60,
        "system_events": 18
      }
    }
    ```
- **`POST /api/v1/simulation/generate`**
  - **Description**: Trigger seeded deterministic record generation.
  - **Request Body**:
    ```json
    {
      "seed": 42,
      "scale": "demo",
      "reset_first": false
    }
    ```
  - **Response 201 Created**:
    ```json
    {
      "message": "Simulation data generated successfully.",
      "seed": 42,
      "scale": "demo",
      "records_created": {
        "sessions": 10,
        "tasks": 60,
        "operations": 120,
        "detections": 350,
        "decisions": 60,
        "system_events": 18
      }
    }
    ```
- **`POST /api/v1/simulation/reset`**
  - **Description**: Safely purges simulated records. Requires explicit confirmation header/body.
  - **Request Body**:
    ```json
    {
      "confirm_purge": true,
      "purge_target": "SIMULATED_ONLY"
    }
    ```

### 3.3 Sessions (`/api/v1/sessions`)
- **`GET /api/v1/sessions`**
  - **Query Params**: `status`, `environment`, `limit` (default 50), `offset` (default 0).
  - **Response 200 OK**: Array of session objects.
- **`GET /api/v1/sessions/{session_id}`**
  - **Response 200 OK**: Full session object including summary task and operation counts.

### 3.4 Tasks (`/api/v1/tasks`)
- **`GET /api/v1/tasks`**
  - **Query Params**: `session_id`, `task_status`, `priority`, `task_type`, `limit`, `offset`.
  - **Response 200 OK**: Array of task objects.
- **`GET /api/v1/tasks/{task_id}`**
  - **Response 200 OK**: Detailed task object with linked operations and decision.

### 3.5 Detections (`/api/v1/detections`)
- **`GET /api/v1/detections`**
  - **Query Params**: `session_id`, `class_label`, `min_confidence` (float 0.0-1.0), `limit` (default 50), `offset`.
  - **Response 200 OK**: Array of detection objects from MongoDB.
- **`GET /api/v1/detections/{detection_id}`**
  - **Response 200 OK**: Single detection document including bounding box and metadata.

### 3.6 Operations (`/api/v1/operations`)
- **`GET /api/v1/operations`**
  - **Query Params**: `task_id`, `device_id`, `operation_status`, `operation_type`, `limit`, `offset`.
  - **Response 200 OK**: Array of operation records from MySQL.

### 3.7 Decisions (`/api/v1/decisions`)
- **`GET /api/v1/decisions`**
  - **Query Params**: `session_id`, `task_id`, `decision_type`, `limit`, `offset`.
  - **Response 200 OK**: Array of decision records with `rationale`.

### 3.8 System Events (`/api/v1/system-events`)
- **`GET /api/v1/system-events`**
  - **Query Params**: `event_type`, `resolution_status`, `device_id`, `limit`, `offset`.
  - **Response 200 OK**: Array of system event records.
- **`PATCH /api/v1/system-events/{event_id}`**
  - **Request Body**:
    ```json
    {
      "resolution_status": "RESOLVED"
    }
    ```
  - **Response 200 OK**: Updated system event record.

### 3.9 Analytics and Summaries (`/api/v1/analytics`)
- **`GET /api/v1/analytics/overview`**
  - **Response 200 OK**: Aggregated counts for dashboard KPI cards.
- **`GET /api/v1/analytics/produce-classes`**
  - **Response 200 OK**: Distribution of produce grades (`GRADE_A`, `GRADE_B`, `BLEMISHED`, etc.) across detections.
- **`GET /api/v1/analytics/operation-outcomes`**
  - **Response 200 OK**: Success, failure, and timeout ratios by operation type.

### 3.10 Equipment & Models (`/api/v1/devices`, `/api/v1/models`)
- **`GET /api/v1/devices`**: Returns list of physical handling devices and cameras.
- **`GET /api/v1/models`**: Returns list of registered AI models and versions.

