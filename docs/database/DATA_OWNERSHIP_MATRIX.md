# Data Ownership and Storage Allocation Matrix

## 1. Overview
This matrix governs the allocation of entities and payloads between **MySQL 8.4 LTS** (Relational Database) and **MongoDB Community Server 8.0** (Document Database).

The allocation reconciles the conceptual ER diagram, relational 3NF schema, and DFD Level 1/2 process descriptions.

---

## 2. Store Allocation Matrix

| Data Category / Entity | Primary Store | Authoritative Copy | Secondary Store (if any) | Linking Key / Reference Strategy | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **SESSION** | MySQL 8.4 | **MySQL** (`session` table) | None | N/A | **CONFIRMED** |
| **TASK** | MySQL 8.4 | **MySQL** (`task` table) | None | `session_id` FK | **CONFIRMED** |
| **OPERATION** | MySQL 8.4 | **MySQL** (`operation` table) | None | `task_id` FK, `device_id` FK | **CONFIRMED** |
| **DECISION** | MySQL 8.4 | **MySQL** (`decision` table) | None | `session_id` FK, `task_id` FK (nullable) | **CONFIRMED** |
| **DEVICE** | MySQL 8.4 | **MySQL** (`device` table) | None | N/A | **CONFIRMED** |
| **AI_MODEL** | MySQL 8.4 | **MySQL** (`ai_model` table) | Optional MongoDB config store | `model_id` | **CONFIRMED** |
| **DETECTION** | MongoDB 8.0 | **MongoDB** (`detections` collection) | None (or lean SQL stub) | Documents store `session_id`, `model_id`, `device_id` referencing MySQL PKs | **PROPOSED / NEEDS_DECISION** |
| **SYSTEM_EVENT** | MySQL 8.4 | **MySQL** (`system_event` table) | MongoDB (`telemetry_logs` for unstructured/high-frequency logs) | MySQL stores structured operational events; MongoDB stores raw device telemetry streams | **PROPOSED / NEEDS_DECISION** |

---

## 3. Detailed Data Store Justification

### 3.1 Relational Store: MySQL 8.4 LTS
- **Why MySQL for Sessions, Tasks, Decisions, Operations, and Devices?**
  - High degree of structural stability, strict 3NF relationships, and foreign key integrity.
  - Transactions across task lifecycles and operational status transitions require ACID guarantees.
  - Analytical aggregations (e.g., session durations, task completion rates, device fault ratios) are natively executed with SQL joins and index scans.

### 3.2 Document Store: MongoDB Community Server 8.0
- **Why MongoDB for Detections and Telemetry?**
  - **Detections**: Produce inspection yields variable vision outputs: bounding box coordinates, multidimensional confidence scores, feature embeddings, class taxonomies, and detector hyperparameters. A JSON BSON document schema provides flexibility without requiring schema migrations for new AI models.
  - **Telemetry Logs**: High-frequency sensor outputs (e.g. IMU readings, motor currents, thermal sensors) produce irregular, nested log records that would inflate relational row locks.

---

## 4. Cross-Store Referential Consistency Strategy

When MongoDB documents reference relational entities in MySQL:
1. **Unidirectional Foreign Reference**: MongoDB documents store relational UUID / Integer keys (`session_id`, `device_id`, `model_id`).
2. **Persistence Sequencing**:
   - Backend services must ensure parent relational records (`session`, `device`, `model`) exist in MySQL **before** persisting associated detection or telemetry documents into MongoDB.
3. **Orphan Prevention**:
   - Deleting a relational `session` record must either cascade via the backend application service to delete corresponding MongoDB documents or be rejected (`ON DELETE RESTRICT`).
4. **Authoritative Principle**:
   - There are **no duplicate authoritative copies**. A detection document in MongoDB is the sole record of truth for that detection observation.

