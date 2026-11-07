# Requirements Specification

## 1. Functional Requirements (FR)

### FR-1: Session Management
- **FR-1.1**: The system shall create, update, and persist operational sessions in MySQL with attributes: `session_id`, `start_time`, `end_time`, `environment`, `session_status`, and `notes`.
- **FR-1.2**: Session status must reflect standard operational states: `INITIALIZING`, `ACTIVE`, `PAUSED`, `COMPLETED`, `ABORTED`.
- **FR-1.3**: The system shall enforce that `start_time <= end_time` for all closed sessions.

### FR-2: Task Lifecycle and Prioritization
- **FR-2.1**: The system shall persist tasks linked to a valid `session_id`.
- **FR-2.2**: Tasks must track `task_type` (e.g. `INSPECTION`, `SORTING`, `PICK_AND_PLACE`), `target_description`, `priority` (e.g. `LOW`, `MEDIUM`, `HIGH`, `CRITICAL`), `creation_time`, `start_time`, `end_time`, and `task_status` (`PENDING`, `IN_PROGRESS`, `COMPLETED`, `FAILED`, `CANCELLED`).
- **FR-2.3**: Tasks must not enforce an accidental self-referencing foreign key on `task_id`.

### FR-3: Operational Decision Tracking
- **FR-3.1**: The system shall record autonomous decision events containing `decision_id`, `decision_time`, `decision_type` (e.g. `GRADING`, `ROUTING_SELECT`, `RETRY`), `selected_action`, `rationale`, and `input_reference`.
- **FR-3.2**: Decisions must link to `session_id` (mandatory) and optionally to `task_id` (nullable).
- **FR-3.3**: The schema shall not contain a column named `rescription`.

### FR-4: Device and Equipment Registry
- **FR-4.1**: The system shall maintain an equipment registry in MySQL with attributes: `device_id`, `device_name`, `device_type` (e.g. `RGB_CAMERA`, `DEPTH_SENSOR`, `ROBOTIC_ARM`, `AGV_CHASSIS`), `device_status` (`ONLINE`, `OFFLINE`, `CALIBRATING`, `FAULT`), and `description`.
- **FR-4.2**: Devices shall be linkable to operations and system events.

### FR-5: Operation Execution and Verification
- **FR-5.1**: The system shall record physical handling operations containing `operation_id`, `operation_type` (e.g. `GRASP`, `LIFT`, `TRANSPORT`, `RELEASE`), `start_time`, `end_time`, `operation_status` (`IN_PROGRESS`, `SUCCESS`, `FAILURE`, `TIMEOUT`), and `result` (e.g. JSON or text outcome summary).
- **FR-5.2**: Operations must link to a parent `task_id` and an executing `device_id`.

### FR-6: Vision Detection Metadata
- **FR-6.1**: The system shall store vision detection records containing `detection_id`, `detection_time`, `class_label` (e.g. `GRADE_A_APPLE`, `BLEMISHED_APPLE`, `DEBRIS`), `confidence_score` (float `[0.0, 1.0]`), `bounding_box` (`ymin, xmin, ymax, xmax`), and `frame_reference`.
- **FR-6.2**: Detections shall reference `session_id`, `model_id`, and `device_id`.
- **FR-6.3**: Detection records shall be stored in MongoDB to accommodate varying model inference outputs.

### FR-7: System Events and Fault Logging
- **FR-7.1**: The system shall record diagnostic and anomaly events containing `event_id`, `event_time`, `event_type` (`INFO`, `WARNING`, `ERROR`, `CRITICAL_FAULT`), `description`, and `resolution_status` (`OPEN`, `ACKNOWLEDGED`, `RESOLVED`, `IGNORED`).
- **FR-7.2**: System events must link to `device_id` and optionally to `operation_id`.

### FR-8: Simulated Data Generation and Ingestion
- **FR-8.1**: The simulator shall generate plausible operational workflows using a deterministic seed.
- **FR-8.2**: All generated records must carry provenance metadata (`provenance = "SIMULATED"`).
- **FR-8.3**: The simulator shall support dataset presets: `small` (1 session, 5 tasks), `medium` (5 sessions, 25 tasks), and `demo` (10 sessions, 60 tasks with normal and fault scenarios).

---

## 2. Non-Functional Requirements (NFR)

- **NFR-1: Data Integrity & Consistency**: Relational tables in MySQL 8.4 must enforce 3NF normalization, foreign key constraints, and avoid orphan records.
- **NFR-2: Performance**: API endpoints must return single-session query results within 200ms under standard demo dataset volume.
- **NFR-3: Security & Secret Isolation**: Database credentials must be loaded exclusively via environment variables; client code must have zero access to database credentials or raw connection strings.
- **NFR-4: Modularity**: Backend code must strictly decouple routes (`api/`), models/schemas (`schemas/`, `models/`), business logic (`services/`), and data queries (`repositories/`).
- **NFR-5: Accessibility & UX**: Frontend must render responsive views with distinct visual states for loading, empty datasets, API errors, and a persistent simulation indicator.
- **NFR-6: Reproducibility**: The complete system must build and run on Windows 11 with documented setup steps and zero undocumented binary dependencies.

