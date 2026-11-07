# Simulated Operational Data Generator
**Developer Owners**: Rahul (Backend Integration) & Rakshith Raghavendra (Data Architecture)

---

## 1. Overview
The `simulator/` module implements a standalone, deterministic synthetic data generator for the **Post-Harvest DBMS**. It simulates plausible operational sessions, tasks, detections, decisions, operations, and system events for automated post-harvest produce handling.

### Core Rules:
1. **Configurable Seed**: Accepts `--seed <int>` (default `42`) to produce identical datasets across test runs.
2. **Explicit Provenance**: Every generated row or document carries `provenance = "SIMULATED"`.
3. **Plausible Life Cycles**:
   - `session.start_time <= task.start_time <= op.start_time <= op.end_time <= task.end_time <= session.end_time`.
   - Incorporates realistic failure scenarios (~5–12% failure/retry rate) rather than 100% success.
4. **Safe Reset**: Purge operations require `--confirm` before deleting existing simulated data.

---

## 2. Directory Structure
```text
simulator/
├── generators/       # Core generator logic (sessions, detections, tasks, events)
├── scenarios/        # Scenario presets (normal grading, defect handling, gripper slip)
└── README.md         # This documentation file
```

---

## 3. Usage Commands
```powershell
# Run generator with demo profile and default seed 42
python -m simulator.generators.main --seed 42 --scale demo --mode insert

# Run generator with small CI profile
python -m simulator.generators.main --seed 101 --scale small --mode insert

# Reset simulated data only (requires confirmation flag)
python -m simulator.generators.main --reset --confirm
```

