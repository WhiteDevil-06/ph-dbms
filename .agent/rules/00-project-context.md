# Rule 00: Project Context and Identity

## Mandate
This project is titled **"Intelligent Data Management and Operational Analytics for Autonomous Post-Harvest Material Handling Systems"**.
It represents the persistence, monitoring, and analytics layer for an autonomous post-harvest agricultural material-handling system.

## Boundaries
1. **Not a Robot Controller**: This software never executes low-level robot control (e.g., motor actuation, joint kinematics, trajectory planning, real-time safety stops). All physical operations are conducted by an external robotic platform.
2. **Current Project Phase**: Prototype / Simulation phase. The physical robot is currently under construction.
3. **Data Provenance**: There is zero live robot integration in this phase. All ingested operational data is generated via a deterministic, seeded simulation engine and must be explicitly identified as simulated.
4. **No Media Subsystem**: The DBMS stores detection metadata, confidence scores, bounding boxes, and frame identifiers. It does not store raw video or image payloads unless an explicit requirement is approved by the project lead.

