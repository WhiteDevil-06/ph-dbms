# Workflow: Generate Simulation Data

## Owners
Rahul (Backend Integration) & Rakshith Raghavendra (Data Integrity)

## Steps
1. **Check Simulation Specification**:
   - Consult `docs/simulation/SIMULATION_SPEC.md` for generation parameters (seed, scale: small/medium/demo).
2. **Execute Simulator Script**:
   - Run seed generation command:
     ```powershell
     python -m simulator.generators.main --seed 42 --scale demo --mode insert
     ```
3. **Verify Provenance and Integrity**:
   - Query MySQL and MongoDB to confirm all inserted records carry `provenance = 'SIMULATED'`.
   - Verify referential integrity:
     - All `task` records reference valid `session_id`.
     - All `operation` records reference valid `task_id` and `device_id`.
     - All `detection` documents reference valid `session_id`, `model_id`, and `device_id`.
4. **Validate Temporal Sequencing**:
   - Verify start times precede end times across sessions, tasks, and operations.
5. **Verify API & UI Exposure**:
   - Check FastAPI read endpoints: verify records return correctly formatted JSON.
   - Check React dashboard: confirm the "SIMULATION DATA" indicator is prominently displayed.

