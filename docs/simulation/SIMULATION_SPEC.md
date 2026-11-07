# Simulation Specification and Synthetic Data Generator
**Developer Owners**: Rahul (Backend Integration) & Rakshith Raghavendra (Data Architecture)

---

## 1. Objectives and Constraints
In the absence of live physical robotics hardware, the simulation engine (`simulator/`) synthesizes plausible, chronologically ordered, and referentially sound post-harvest operational records.

### Mandatory Rules:
1. **Configurable Seed**: Must support a random seed (e.g. `--seed 42`) producing identical datasets across executions.
2. **Provenance Field**: Every inserted relational row and MongoDB document must explicitly include `provenance = "SIMULATED"`.
3. **Realistic Outcomes**: Must not simulate unrealistically perfect success. Operational failure modes (e.g. gripper slips, detection false positives, camera calibration warnings, robot arm timeouts) must occur at realistic statistical rates (~5–12%).
4. **Temporal Consistency**:
   - `session.start_time <= task.creation_time <= task.start_time <= op.start_time <= op.end_time <= task.end_time <= session.end_time`.
5. **Safe Data Purge**: Resetting or reseeding the database requires an explicit confirmation parameter (`confirm_purge=True`) to prevent accidental data loss.

---

## 2. Plausible Post-Harvest Operational Scenarios

### Scenario A: Normal Grading and Sorting (Apple Packhouse)
1. **Session Starts**: Session `sess-demo-01` initializes in "Packhouse Sorting Bay 2".
2. **Inspection Task**: Vision camera captures produce on conveyor.
3. **Detection Generated**: 3 to 8 detections per frame. Bounding boxes localized, classes assigned (`GRADE_A_APPLE`, `GRADE_B_APPLE`, `BLEMISHED_APPLE`).
4. **Autonomous Decision**: Decision logic assesses detection metadata (`decision_type = "GRADING"`, `selected_action = "ROUTE_TO_GRADE_A_BIN"`, `rationale = "Produce defect area < 2% with diameter 75mm"`).
5. **Sorting Operation**: Robotic manipulator executes `GRASP`, `LIFT`, `TRANSPORT`, and `RELEASE` operations. Status: `SUCCESS`.
6. **Task & Session Complete**: Task marked `COMPLETED`. Session status marked `COMPLETED`.

### Scenario B: Detection Under Confidence Threshold & Secondary Verification
1. **Inspection Task**: Camera captures partially occluded produce (`confidence_score = 0.58`).
2. **Decision**: Decision logic triggers `REINSPECT` (`rationale = "Confidence below 0.70 threshold; produce orientation ambiguous"`).
3. **Secondary Operation**: AGV adjusts camera angle or conveyor moves produce 50mm.
4. **Follow-up Detection**: Secondary detection reaches 0.91 confidence. Sorting proceeds.

### Scenario C: Gripper Slip / Hardware Fault (Exceptional Flow)
1. **Handling Task**: Pick-and-place task initiated.
2. **Operation**: Manipulator attempts `GRASP` on oversized produce.
3. **Fault Trigger**: Suction vacuum sensor reports pressure loss during lift (`operation_status = "FAILURE"`, `result = "GRIPPER_VACUUM_LOSS"`).
4. **System Event Logged**: `system_event` recorded with `event_type = "WARNING"`, `device_id = "robotic_arm_01"`, `description = "Vacuum pressure drop detected during lift phase."`, `resolution_status = "OPEN"`.
5. **Task Outcome**: Task transitions to `FAILED` or initiates retry sequence.

---

## 3. Dataset Scale Profiles

| Preset | Target Sessions | Tasks / Session | Detections / Session | Operations / Task | System Events / Session | Intended Use Case |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`small`** | 1 | 5 | ~20 | 2 | 1-2 | Fast unit tests and CI pipelines |
| **`medium`** | 5 | 10 | ~100 | 2-3 | 3-5 | Local development and component testing |
| **`demo`** | 10 | 12 | ~350 | 2-4 | 8-12 | Academic evaluation, charts, and presentation |

---

## 4. CLI Generator Interface

```powershell
# Generate demo dataset with deterministic seed
python -m simulator.generators.main --seed 42 --scale demo --mode insert

# Reset simulated data only (requires confirmation)
python -m simulator.generators.main --reset --confirm
```

