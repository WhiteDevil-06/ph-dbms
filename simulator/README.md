# Simulated Operational Data Generator
**Developer Owners**: Rahul (Backend Integration) & Rakshith Raghavendra (Data Architecture)

---

## 1. Overview
The `simulator/` module implements a standalone, deterministic synthetic data generator for the **Post-Harvest DBMS**. It simulates plausible operational sessions, tasks, detections, decisions, operations, and system events for automated post-harvest produce handling.

### Core Rules:
1. **Configurable Seed**: Accepts `--seed <int>` (default `42`) to produce identical datasets across test runs.
2. **Explicit Provenance**: Every generated row or document carries `provenance = "SIMULATED"`.
3. **Plausible Life Cycles**:
   - `session.start_time <= task.creation_time <= task.start_time <= op.start_time <= op.end_time <= task.end_time <= session.end_time`.
   - Incorporates realistic failure scenarios (~5–12% failure/retry rate) rather than 100% success.
4. **Safe Reset**: Purge operations require `--confirm` before deleting existing simulated data.

---

## 2. Directory Structure
```text
simulator/
├── generators/
│   ├── data_generator.py      # Core simulation generator logic & dataset synthesizer
│   ├── database_loader.py     # MySQL & MongoDB batch ingestion and purge handler
│   └── main.py                # CLI runner entrypoint
├── scenarios/
│   └── profiles.py            # Scale profiles (small, medium, demo) and hardware catalogs
└── README.md                  # This documentation file
```

---

## 3. Dataset Scale Profiles

| Profile | Sessions | Tasks / Session | Detections / Session | Operations / Task | System Events / Session | Intended Use |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`small`** | 1 | 5 | ~20 | 2 | 2 | Fast unit tests and CI pipelines |
| **`medium`** | 5 | 10 | ~100 | 2 | 4 | Local integration testing |
| **`demo`** | 10 | 12 | ~350 | 3 | 10 | Dashboard evaluation and presentation |

---

## 4. Usage Commands

```powershell
# Run generator with demo profile and default seed 42 (persists to MySQL & MongoDB if connected)
python -m simulator.generators.main --seed 42 --scale demo --mode insert

# Run generator in dry-run mode (synthesizes records and prints counts without DB persistence)
python -m simulator.generators.main --seed 42 --scale demo --mode dry-run

# Run generator and export dataset to a JSON file
python -m simulator.generators.main --seed 42 --scale small --mode export --output simulated_small.json

# Reset simulated data only (requires explicit --confirm flag to prevent accidental loss)
python -m simulator.generators.main --reset --confirm
```

---

## 5. Verification & Tests

To execute the automated test suite verifying seed determinism, temporal consistency, coordinate bounds, and safe purge validation:
```powershell
pytest backend/tests/test_simulation.py -v
```
