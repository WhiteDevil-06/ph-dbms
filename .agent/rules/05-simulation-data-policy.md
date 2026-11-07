# Rule 05: Simulation Data Policy and Provenance

## Mandatory Principles
1. **Explicit Provenance**: Every generated record must contain an explicit provenance attribute:
   - `provenance: "SIMULATED"` (or `"MANUAL_TEST"` for unit test fixtures).
2. **Deterministic Reproducibility**: The simulator must accept a random seed parameter (`seed: int = 42`) to produce identical event sequences and datasets across runs.
3. **Persistent UI Indicator**: Whenever simulated data is displayed in the dashboard, a prominent, persistent badge or banner labelled `"SIMULATION DATA"` must remain visible across all pages.
4. **Honest Reporting**:
   - Never label simulated records as real-world physical operations, live robot telemetry, or genuine field results.
   - Never claim physical robotic throughput or hardware cycle time benchmarks based on synthetic generator performance.
5. **Plausible Coherence**: Generated records must respect realistic chronological order:
   - `session.start_time` <= `task.start_time` <= `operation.start_time` <= `operation.end_time` <= `session.end_time`.
   - Detection confidence scores must fall within `[0.00, 1.00]`.
   - Bounding boxes must satisfy normalized `[ymin, xmin, ymax, xmax]` constraints.
6. **Safe Reset Operations**: Any simulator command or API endpoint that clears or reseeds the database must require explicit safety confirmation and must never run automatically on production-configured databases.

