# Architecture Audit and Source Diagram Analysis

## 1. Executive Summary and Audit Scope
This document records an exhaustive comparative audit of the three primary source diagrams located in `docs/diagrams/`:
- `ER_DIAGRAM_SOURCE.jpg`
- `DFD_LEVELS_SOURCE.jpg`
- `RELATIONAL_SCHEMA_SOURCE.jpg`

The purpose of this audit is to systematically expose ambiguities, graphical drafting anomalies, structural discrepancies, and cross-model conflicts **before** any physical database schema or backend code is implemented.

---

## 2. Epistemic Classification of Diagram Contents

### 2.1 Confirmed Source Facts (ER Diagram)
- **Entities & Attributes**:
  - `SESSION` (`session_id` [PK], `start_time`, `end_time`, `environment`, `session_status`, `notes`)
  - `TASK` (`task_id` [PK], `task_type`, `target_description`, `priority`, `creation_time`, `start_time`, `end_time`, `task_status`)
  - `OPERATION` (`operation_id` [PK], `operation_type`, `start_time`, `end_time`, `operation_status`, `result`)
  - `DECISION` (`decision_id` [PK], `decision_time`, `decision_type`, `selected_action`, `rationale`, `input_reference`)
  - `DEVICE` (`device_id` [PK], `device_name`, `device_type`, `device_status`, `description`)
  - `AI_MODEL` (`model_id` [PK], `model_name`, `model_version`, `configuration`, `created_at`)
  - `DETECTION` (`detection_id` [PK], `detection_time`, `class_label`, `confidence_score`, `bounding_box`, `frame_reference`)
  - `SYSTEM_EVENT` (`event_id` [PK], `event_time`, `event_type`, `description`, `resolution_status`)
- **Direct ER Relationships**:
  - `SESSION [1]` contains `[N] TASK`
  - `SESSION [1]` contains `[N] DETECTION`
  - `SESSION [1]` records `[N] DECISION`
  - `TASK [1]` includes `[N] OPERATION`
  - `AI_MODEL [1]` generates `[N] DETECTION`
  - `DEVICE [1]` captures `[0..N] DETECTION`
  - `OPERATION [1]` is associated with `[0..N] SYSTEM_EVENT`

---

## 3. Discrepancy & Anomaly Audit Register

| ID | Source Diagram(s) | Issue / Observation | Why It Matters | Safe Interpretation (if any) | Proposed Resolution | Approval Required? | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **AUD-01** | `RELATIONAL_SCHEMA_SOURCE.jpg` | `TASK` table lists both `PK task_id` and `FK task_id`. | An FK pointing to the same table's PK creates an unintended recursive self-reference, preventing normal task creation without complex self-referencing hierarchy. | In the ER diagram, `SESSION [1]` contains `[N] TASK`. In the schema, `FK session_id` is present, but `FK task_id` was accidentally duplicated in the column list. | Remove `FK task_id` from `TASK`. Retain `PK task_id` and `FK session_id` referencing `SESSION(session_id)`. | **Yes (Project Lead)** | **RESOLVED (DEC-01 Approved)** |
| **AUD-02** | `RELATIONAL_SCHEMA_SOURCE.jpg` vs `ER_DIAGRAM_SOURCE.jpg` | Schema image includes an attribute named `rescription` in `DECISION` alongside `rationale`. ER diagram shows only `rationale`. | `rescription` appears to be a clerical spelling typo for `description` or accidental duplication of `rationale`. Implementing both causes redundant or dead schema fields. | The conceptual intent is to capture the explanation or justification for an autonomous decision. `rationale` is standard. | Eliminate column `rescription`. Maintain `rationale TEXT` as the authoritative field in `DECISION`. | **Yes (Project Lead)** | **RESOLVED (DEC-02 Approved)** |
| **AUD-03** | `RELATIONAL_SCHEMA_SOURCE.jpg` vs `ER_DIAGRAM_SOURCE.jpg` | In `RELATIONAL_SCHEMA`, `OPERATION` has foreign keys `FK task_id` and `FK device_id`. In `ER_DIAGRAM`, there is no direct line/relationship between `OPERATION` and `DEVICE`. | If `OPERATION` requires `device_id`, the physical execution device (e.g. robotic arm, conveyor motor) is explicitly tracked per operation. The ER diagram omitted this direct relationship diamond. | In a physical material handling cell, an operation is performed by a specific physical device/actuator. Linking `OPERATION` to `DEVICE` is functionally essential. | Approve adding `FK device_id` on `OPERATION` referencing `DEVICE(device_id)`. Note update in ER documentation. | **Yes (Project Lead)** | **RESOLVED (DEC-03 Approved)** |
| **AUD-04** | `DFD_LEVELS_SOURCE.jpg` vs `RELATIONAL_SCHEMA_SOURCE.jpg` | In DFD Level 1, `DETECTION` is mapped to `D2: MongoDB Database (Detection & Event Data)`. However, `RELATIONAL_SCHEMA` depicts `DETECTION` as a relational 3NF table with foreign keys (`session_id`, `model_id`, `device_id`). | Having detection data modeled both as a strict relational SQL table and as a flexible NoSQL document collection creates architecture confusion regarding data ownership and query responsibility. | Object detections in vision-guided handling produce variable-length metadata (e.g., confidence arrays, bounding boxes, segmentation masks) best suited for MongoDB, while summary foreign keys link back to relational sessions. | Adopt MongoDB as authoritative store for `DETECTION` documents (`detections` collection). Store foreign references (`session_id`, `model_id`, `device_id`) inside the document. Do not create a MySQL `detection` table, or keep MySQL as an optional lean metadata index. | **Yes (Team)** | **RESOLVED (DEC-04 Approved)** |
| **AUD-05** | `DFD_LEVELS_SOURCE.jpg`, `ER_DIAGRAM_SOURCE.jpg`, `RELATIONAL_SCHEMA_SOURCE.jpg` | `SYSTEM_EVENT` appears in both `D1: MySQL Database` and `D2: MongoDB Database` in DFD Level 1. In ER, line routing to `SYSTEM_EVENT` from `DEVICE` has two diamonds (`logs` and `performs`) with crossing lines from `TASK`. In Schema, `SYSTEM_EVENT` has `FK operation_id` and `FK device_id`. | Storing duplicate system events across two databases creates split-brain state without a synchronization mechanism. Ambiguous ER lines obscure whether events originate from tasks, devices, or operations. | Relational DB should store operational lifecycle events with structured status (`resolution_status`), while MongoDB stores unstructured high-frequency hardware telemetry logs. | Allocate structured `system_event` to MySQL with `FK operation_id` (nullable) and `FK device_id` (not null). Direct raw sensor/telemetry streams to MongoDB `telemetry_logs`. | **Yes (Team)** | **RESOLVED (DEC-05 Approved)** |
| **AUD-06** | `DFD_LEVELS_SOURCE.jpg` (Level 2) | In Level 2 DFD, processes `1.0 Collect and Validate Data` and `3.0 Retrieve Data and Generate Reports` are drawn inside the dashed decomposition boundary of `Process 2.0 - Manage Operational Records`. Also contains typos: "Retnieved records", "Read ved structured records". | In standard Yourdon/DeMarco DFD notation, decomposing Process 2.0 should only contain subprocesses numbered 2.1, 2.2, 2.3, etc. Processes 1.0 and 3.0 are adjacent peer processes, not children of 2.0. | The diagram author drew peer processes inside the visual boundary to illustrate data flow continuity. | Document the academic diagram anomaly without altering the source image. In architecture docs, represent 1.0 and 3.0 as external/peer processes connecting to subprocesses 2.1, 2.2, and 2.3. | No | **MINOR (Documented)** |
| **AUD-07** | `ER_DIAGRAM_SOURCE.jpg` | `DECISION` relationship: ER diagram shows `SESSION [1] - records - [N] DECISION` and `TASK [0..N] - may initiate - [0..1] DECISION`. Relational schema shows `DECISION` having both `FK session_id` and `FK task_id`. | ER cardinality labels near TASK (`0..N`) and DECISION (`0..1`) can be interpreted in opposite directions depending on notation style (Chen vs Crow's Foot). Does a task initiate up to 1 decision, or can a decision be initiated by multiple tasks? | In robotics workflow: Vision → Detection → Decision → Task/Operation. A decision belongs to a session and optionally initiates or guides a specific task. Thus `task_id` in `DECISION` should be a nullable foreign key. | Confirm `DECISION` table in MySQL carries `FK session_id` (NOT NULL) and `FK task_id` (NULLABLE). | **Yes (Project Lead)** | **RESOLVED (DEC-05 Approved)** |
| **AUD-08** | `ER_DIAGRAM_SOURCE.jpg` | `bounding_box` attribute in `DETECTION`: source diagram defines it as a single attribute. | In relational databases, storing coordinates in a single column requires custom parsing (e.g. comma-separated string) or JSON. In MongoDB, it naturally maps to a nested document or array `[ymin, xmin, ymax, xmax]`. | Reinforces MongoDB as the natural target for `DETECTION` records. | Use MongoDB document schema with nested `bounding_box: { ymin, xmin, ymax, xmax }`. | **Yes (Team)** | **RESOLVED (DEC-04 Approved)** |

---

## 4. Decisions Required from the Project Team Before Schema Implementation

Before Rakshith executes DDL migrations and Rahul implements database repositories, the project team must formally confirm and record decisions for the following items in `docs/decisions/DECISION_LOG.md`:

1. **[DEC-01] Self-Referencing FK in TASK**: Confirm removal of `FK task_id` from `TASK` so `task_id` is strictly the primary key, and `session_id` is the parent foreign key.
2. **[DEC-02] Typo Removal in DECISION**: Confirm omission of `rescription` and adoption of `rationale TEXT` as the authoritative column.
3. **[DEC-03] OPERATION to DEVICE Foreign Key**: Confirm inclusion of `device_id` as a foreign key on `OPERATION`.
4. **[DEC-04] Authoritative Data Store Allocation (DETECTION & SYSTEM_EVENT)**:
   - Confirm whether `DETECTION` resides exclusively in MongoDB Community Server 8.0 or if a relational stub table is maintained in MySQL.
   - Confirm whether `SYSTEM_EVENT` resides in MySQL as structured operational events, with raw telemetry in MongoDB `telemetry_logs`.
5. **[DEC-05] Nullability of Foreign Keys**:
   - Confirm `DECISION.task_id` is nullable (a decision can occur at the session level before a specific task is spawned).
   - Confirm `SYSTEM_EVENT.operation_id` is nullable (system events can be device-level without an active operation).

