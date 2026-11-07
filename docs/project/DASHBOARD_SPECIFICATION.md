# Frontend Dashboard Specification
**Developer Owner**: Ramcharan (Frontend and Dashboard Developer)

---

## 1. Overview and Design Principles

The dashboard provides operators, engineers, and researchers with real-time operational visibility into the post-harvest autonomous material handling system.

### Core Design Rules:
1. **Persistent Simulation Banner**: A fixed, high-contrast banner must appear across the top of every dashboard view stating:
   ```text
   [ SIMULATION DATA ACTIVE ] All telemetry, tasks, and detections are generated from simulated models.
   ```
   Never display fake "Live Hardware Connected" or misleading sensor status badges.
2. **State Completeness**: Every view and data widget must provide explicit UI states:
   - **Loading**: Skeleton placeholder or accessible progress indicator.
   - **Empty**: Informative message when zero records exist (with button to trigger demo seed if enabled).
   - **Error**: Friendly alert message detailing network/API issue without exposing backend stack traces.
3. **Data Boundary**: Frontend components consume only endpoints defined in [API_CONTRACT.md](file:///c:/Users/raksh/OneDrive/Desktop/Post-Harvest-DBMS/docs/api/API_CONTRACT.md). No direct database queries or credentials exist in browser memory.

---

## 2. Page Specifications

### Page 1: Overview / Mission Control
- **Purpose**: High-level operational summary of active and completed sessions.
- **Components**:
  - **KPI Summary Cards**: Total Sessions, Active Tasks, Completed Operations, Open System Events, Average Detection Confidence.
  - **Operation Outcomes Chart**: Donut chart showing distribution of operation results (`SUCCESS`, `FAILURE`, `TIMEOUT`).
  - **Recent Activity Stream**: Chronological feed of the last 10 tasks/events with status badges and timestamps.
  - **Quick Action Bar**: Button to trigger deterministic simulation seed generation (calls `POST /api/v1/simulation/generate`).

### Page 2: Sessions Explorer
- **Purpose**: Manage and inspect operational session lifecycles.
- **Components**:
  - **Filter Controls**: Status dropdown (`INITIALIZING`, `ACTIVE`, `COMPLETED`, `ABORTED`), date-time range picker, environment text filter.
  - **Sessions Table**: Columns for `session_id`, `environment`, `start_time`, `end_time`, `duration`, `session_status`, and `notes`.
  - **Session Detail Drawer**: Slide-over panel revealing associated tasks, decisions, and aggregated metrics for the selected session.

### Page 3: Task Management
- **Purpose**: Track post-harvest task queues, priorities, and lifecycles.
- **Components**:
  - **Task Kanban / List View**: Grouped or filterable by `task_status` (`PENDING`, `IN_PROGRESS`, `COMPLETED`, `FAILED`).
  - **Table Columns**: `task_id`, `task_type` (e.g. `INSPECTION`, `SORTING`), `target_description`, `priority` (color-coded badges: Low/Med/High/Critical), `creation_time`, `start_time`, `end_time`, `session_id`.
  - **Task Timeline**: Visual timeline indicating duration between `creation_time`, `start_time`, and `end_time`.

### Page 4: Vision & Detections
- **Purpose**: Inspect vision inference metadata and quality classifications.
- **Components**:
  - **Notice**: "Detections represent individual spatial observations. Inter-frame object tracking is not supported."
  - **Filters**: Class label filter (`GRADE_A`, `GRADE_B`, `BLEMISHED`, `FOREIGN_OBJECT`), confidence threshold slider (0.0 to 1.0), session filter.
  - **Detections Grid / Table**:
    - `detection_id`, `detection_time`, `class_label`, `confidence_score` (progress bar), `bounding_box` (`[ymin, xmin, ymax, xmax]`), `frame_reference`, `model_id`, `device_id`.
  - **Spatial Preview Widget**: Canvas/SVG rendering normalized bounding boxes on a simulated produce grid based on coordinates.

### Page 5: Operations & Actuation
- **Purpose**: Audit physical execution steps performed by robotic manipulators and AGVs.
- **Components**:
  - **Filter Controls**: Operation type (`GRASP`, `LIFT`, `TRANSPORT`, `RELEASE`), execution device, outcome status (`SUCCESS`, `FAILURE`).
  - **Operations Table**: `operation_id`, `task_id`, `device_id`, `operation_type`, `start_time`, `end_time`, `duration_seconds`, `operation_status`, `result`.
  - **Duration Distribution Histogram**: Visual chart showing execution duration across operation types.

### Page 6: Operational Decisions
- **Purpose**: Review autonomous decision logic and action selection rationale.
- **Components**:
  - **Decisions Table**: `decision_id`, `decision_time`, `decision_type` (e.g. `GRADING`, `SORT_ROUTE`), `selected_action`, `rationale`, `input_reference`, `session_id`, `task_id`.
  - **Audit Detail Modal**: Deep dive into the decision rationale and input reference payload.

### Page 7: System Events & Diagnostics
- **Purpose**: System health, fault detection, and incident resolution tracking.
- **Components**:
  - **Severity Badges**: Color-coded severity (`INFO` [blue], `WARNING` [yellow], `ERROR` [orange], `CRITICAL_FAULT` [red]).
  - **Events Table**: `event_id`, `event_time`, `event_type`, `description`, `device_id`, `operation_id`, `resolution_status` (`OPEN`, `ACKNOWLEDGED`, `RESOLVED`).
  - **Status Action**: Button to toggle event `resolution_status` via `PATCH /api/v1/system-events/{event_id}`.

### Page 8: Analytics & Operational Reports
- **Purpose**: Macro-level performance trends and academic evaluation metrics.
- **Components**:
  - **Produce Quality Distribution**: Bar chart comparing detected produce grade classes across sessions.
  - **Operation Success Rate Over Time**: Line chart showing success percentage trends across simulation batches.
  - **Cycle Time Analysis**: Box plot / bar chart of average handling times per produce category.
  - **Export Action**: CSV export of aggregated session metrics (pending approval).

### Page 9: Equipment & Model Registry
- **Purpose**: View registered hardware devices and AI model versions.
- **Components**:
  - **Device List**: `device_id`, `device_name`, `device_type`, `device_status` (Online/Offline/Calibrating/Fault), `description`.
  - **AI Model Catalog**: `model_id`, `model_name`, `model_version`, `configuration`, `created_at`.

