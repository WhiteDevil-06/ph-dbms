# Scope and Objectives

## 1. Project Objectives
1. **Unified Operational Persistence**: Provide a persistent, queryable data store for all phases of autonomous post-harvest operations (sessions, tasks, detections, decisions, operations, devices, system events).
2. **Hybrid Dual-Store Architecture**: Leverage MySQL 8.4 LTS for structured, relational operational workflows and MongoDB Community Server 8.0 for flexible, semi-structured vision detections and event logs.
3. **Plausible Deterministic Simulation**: Build a standalone data simulator generating chronologically valid, referentially sound operational datasets with configurable seeds.
4. **Standardized API Gateway**: Expose FastAPI REST endpoints providing validated JSON data for analytics, filtering, and reporting.
5. **Operational Analytics Dashboard**: Deliver a responsive React (TypeScript/Tailwind CSS) web dashboard displaying operational KPIs, status histories, and detection analytics.

---

## 2. In-Scope Deliverables
- **Relational Schema (MySQL 8.4)**: Normalized 3NF tables, primary and foreign keys, indexes, migration scripts, and baseline seeds.
- **Document Store (MongoDB 8.0)**: Collection schemas and indexes for detection metadata and telemetry logs.
- **Backend API (FastAPI)**: REST endpoints covering CRUD operations, filtering, metrics aggregation, and simulation data generation/reset.
- **Simulated Generator (`simulator/`)**: Configurable generator supporting small, medium, and demo datasets, plausible failure scenarios, and deterministic seeds.
- **Web Dashboard (`frontend/`)**: Overview, Sessions, Tasks, Detections, Operations, Decisions, Events, and Analytics views.
- **Documentation & Audit**: Architectural audit, ER-to-Relational mapping, data ownership matrix, API contract, and decision logs.

---

## 3. Explicitly Out-of-Scope
- **Real-Time Robot Control**: Motor speed, wheel navigation, PID control loops, robotic arm trajectory planning, and gripper servo controls.
- **Live Hardware Telemetry**: Live serial, ROS2, CAN bus, or MQTT connections to unfinished physical robotics hardware.
- **Binary Image/Video Storage**: Object storage buckets (AWS S3, MinIO, Google Cloud Storage) for high-resolution images or video streams.
- **Complex Cloud Infrastructure**: Kubernetes clusters, Kafka event brokers, Redis caching layers, distributed service meshes, or commercial cloud databases.
- **Production User Auth / RBAC**: External OAuth2 providers, Okta, or multi-tenant user authentication (beyond basic local dev tokens if needed).

