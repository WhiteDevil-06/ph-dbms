---
name: simulation-testing
description: Execute deterministic, seeded data generation, validate relational and document references, and verify simulation provenance.
---

# Simulation Testing Skill

Use this skill when generating mock/simulation datasets, running integrity checks on simulated event chains, and testing data reset capabilities.

## Core Directives
1. **Configurable Seed**: Always support `--seed <int>` to ensure test runs are 100% reproducible.
2. **Provenance Tagging**: Validate that every inserted row or document contains `provenance = 'SIMULATED'`.
3. **Plausible Workflow Chains**: Verify that generated sessions, tasks, detections, decisions, operations, and system events have chronologically coherent timestamps.
4. **Primary References**:
   - [SIMULATION_SPEC.md](file:///c:/Users/raksh/OneDrive/Desktop/Post-Harvest-DBMS/docs/simulation/SIMULATION_SPEC.md)
   - [simulator/README.md](file:///c:/Users/raksh/OneDrive/Desktop/Post-Harvest-DBMS/simulator/README.md)

