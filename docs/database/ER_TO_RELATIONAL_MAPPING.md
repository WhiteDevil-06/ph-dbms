# ER to Relational Schema Mapping Specification

## 1. Overview
This document maps each entity, attribute, and relationship from `ER_DIAGRAM_SOURCE.jpg` to the proposed physical relational tables depicted in `RELATIONAL_SCHEMA_SOURCE.jpg`, systematically documenting discrepancies and foreign key mappings.

---

## 2. Entity-to-Table Mapping Summary

| ER Entity | Relational Table | Primary Key (Source) | Source Attributes | Proposed Relational Foreign Keys | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **SESSION** | `session` | `session_id` | `start_time`, `end_time`, `environment`, `session_status`, `notes` | None | **CONFIRMED** |
| **TASK** | `task` | `task_id` | `task_type`, `target_description`, `priority`, `creation_time`, `start_time`, `end_time`, `task_status` | `session_id` (FK to `session`) | **CONFLICTING** (Schema shows erroneous `FK task_id`) |
| **DECISION** | `decision` | `decision_id` | `decision_time`, `decision_type`, `selected_action`, `rationale`, `input_reference` | `session_id` (FK to `session`), `task_id` (FK to `task`, nullable) | **CONFLICTING** (Schema shows typo `rescription`) |
| **OPERATION** | `operation` | `operation_id` | `operation_type`, `start_time`, `end_time`, `operation_status`, `result` | `task_id` (FK to `task`), `device_id` (FK to `device`) | **NEEDS_DECISION** (ER omitted direct line to `device`) |
| **DEVICE** | `device` | `device_id` | `device_name`, `device_type`, `device_status`, `description` | None | **CONFIRMED** |
| **AI_MODEL** | `ai_model` | `model_id` | `model_name`, `model_version`, `configuration`, `created_at` | None | **CONFIRMED** |
| **DETECTION** | `detection` | `detection_id` | `detection_time`, `class_label`, `confidence_score`, `bounding_box`, `frame_reference` | In Schema: `session_id`, `model_id`, `device_id`. In DFD: mapped to MongoDB. | **CONFLICTING** (Dual SQL/NoSQL modeling) |
| **SYSTEM_EVENT** | `system_event` | `event_id` | `event_time`, `event_type`, `description`, `resolution_status` | `device_id` (FK to `device`), `operation_id` (FK to `operation`, nullable) | **AMBIGUOUS** (ER lines cross and show two diamonds: `logs` and `performs`) |

---

## 3. Detailed Relationship Analysis

### 3.1 Relationship: `contains` (SESSION - TASK)
- **Entities**: `SESSION` and `TASK`
- **Cardinality (Source)**: `SESSION [1]` to `TASK [N]`
- **Participation**: Total on `TASK` (every task must belong to a session); Partial on `SESSION` (a new session may contain 0 tasks initially).
- **Relational Mapping**: Foreign key `session_id` placed on `TASK` table referencing `SESSION(session_id)`.
- **Status**: **CONFIRMED**.
- **Note on Discrepancy**: The schema diagram depicts `FK task_id` inside `TASK` alongside `PK task_id`. This is an accidental recursive self-reference and must be omitted.

### 3.2 Relationship: `contains` (SESSION - DETECTION)
- **Entities**: `SESSION` and `DETECTION`
- **Cardinality (Source)**: `SESSION [1]` to `DETECTION [N]`
- **Relational Mapping**: If stored in MySQL, `session_id` is an FK in `DETECTION`. If stored in MongoDB, `session_id` is a required top-level field in the detection document.
- **Status**: **NEEDS_DECISION** (pending final data store allocation).

### 3.3 Relationship: `records` (SESSION - DECISION)
- **Entities**: `SESSION` and `DECISION`
- **Cardinality (Source)**: `SESSION [1]` to `DECISION [N]`
- **Relational Mapping**: Foreign key `session_id` placed on `DECISION` table referencing `SESSION(session_id)`.
- **Status**: **CONFIRMED**.

### 3.4 Relationship: `may initiate` (TASK - DECISION)
- **Entities**: `TASK` and `DECISION`
- **Cardinality (Source)**: `TASK [0..N]` to `DECISION [0..1]`
- **Relational Mapping**: Foreign key `task_id` placed on `DECISION` referencing `TASK(task_id)`. Because a decision can be made at the session level before a task is initialized, `task_id` must be `NULLABLE`.
- **Status**: **IMPORTANT / NEEDS_DECISION**.

### 3.5 Relationship: `includes` (TASK - OPERATION)
- **Entities**: `TASK` and `OPERATION`
- **Cardinality (Source)**: `TASK [1]` to `OPERATION [N]`
- **Relational Mapping**: Foreign key `task_id` placed on `OPERATION` referencing `TASK(task_id)`.
- **Status**: **CONFIRMED**.

### 3.6 Relationship: `captures` (DEVICE - DETECTION)
- **Entities**: `DEVICE` and `DETECTION`
- **Cardinality (Source)**: `DEVICE [1]` to `DETECTION [0..N]`
- **Relational Mapping**: Foreign reference `device_id` placed on `DETECTION`.
- **Status**: **CONFIRMED**.

### 3.7 Relationship: `generates` (AI_MODEL - DETECTION)
- **Entities**: `AI_MODEL` and `DETECTION`
- **Cardinality (Source)**: `AI_MODEL [1]` to `DETECTION [N]`
- **Relational Mapping**: Foreign reference `model_id` placed on `DETECTION`.
- **Status**: **CONFIRMED**.

### 3.8 Relationship: `is associated with` (OPERATION - SYSTEM_EVENT)
- **Entities**: `OPERATION` and `SYSTEM_EVENT`
- **Cardinality (Source)**: `OPERATION [1]` to `SYSTEM_EVENT [0..N]`
- **Relational Mapping**: Foreign key `operation_id` placed on `SYSTEM_EVENT` referencing `OPERATION(operation_id)`. Must be `NULLABLE` as system events can occur independently of an active operation.
- **Status**: **CONFIRMED**.

### 3.9 Relationships: `logs` and `performs` (DEVICE / TASK - SYSTEM_EVENT)
- **Entities**: `DEVICE`, `TASK`, and `SYSTEM_EVENT`
- **Source Observations**: The ER diagram depicts two diamonds (`logs` and `performs`) with overlapping lines between `DEVICE`, `TASK`, and `SYSTEM_EVENT`. The schema diagram simplifies this by giving `SYSTEM_EVENT` two foreign keys: `operation_id` and `device_id`.
- **Relational Mapping**: Foreign key `device_id` on `SYSTEM_EVENT` referencing `DEVICE(device_id)`.
- **Status**: **AMBIGUOUS (Source) / RESOLVED IN SCHEMA AS FK device_id**.

