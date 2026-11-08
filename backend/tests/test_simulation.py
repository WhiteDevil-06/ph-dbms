"""Tests for deterministic simulation data generator."""

import pytest
from simulator.generators.data_generator import SimulationGenerator
from simulator.generators.database_loader import reset_simulated_data


def test_simulation_determinism():
    """Verify that identical seeds produce identical datasets."""
    gen1 = SimulationGenerator(seed=42, scale="small")
    ds1 = gen1.generate()

    gen2 = SimulationGenerator(seed=42, scale="small")
    ds2 = gen2.generate()

    assert ds1.counts == ds2.counts
    assert len(ds1.sessions) == len(ds2.sessions)
    assert ds1.sessions[0]["session_id"] == ds2.sessions[0]["session_id"]
    assert ds1.tasks[0]["task_id"] == ds2.tasks[0]["task_id"]
    assert ds1.detections[0]["detection_id"] == ds2.detections[0]["detection_id"]


def test_simulation_seed_variation():
    """Verify that distinct seeds produce different datasets."""
    gen1 = SimulationGenerator(seed=42, scale="small")
    ds1 = gen1.generate()

    gen2 = SimulationGenerator(seed=99, scale="small")
    ds2 = gen2.generate()

    assert ds1.sessions[0]["session_id"] != ds2.sessions[0]["session_id"]


def test_all_records_carry_simulated_provenance():
    """Verify that every relational record and MongoDB document carries provenance='SIMULATED'."""
    generator = SimulationGenerator(seed=42, scale="small")
    ds = generator.generate()

    for item in ds.devices:
        assert item["provenance"] == "SIMULATED"
    for item in ds.models:
        assert item["provenance"] == "SIMULATED"
    for item in ds.sessions:
        assert item["provenance"] == "SIMULATED"
    for item in ds.tasks:
        assert item["provenance"] == "SIMULATED"
    for item in ds.decisions:
        assert item["provenance"] == "SIMULATED"
    for item in ds.operations:
        assert item["provenance"] == "SIMULATED"
    for item in ds.system_events:
        assert item["provenance"] == "SIMULATED"
    for item in ds.detections:
        assert item["provenance"] == "SIMULATED"
    for item in ds.telemetry_logs:
        assert item["provenance"] == "SIMULATED"


def test_temporal_consistency():
    """Verify session.start <= task.creation <= task.start <= op.start <= op.end <= task.end <= session.end."""
    generator = SimulationGenerator(seed=42, scale="medium")
    ds = generator.generate()

    sessions_map = {s["session_id"]: s for s in ds.sessions}
    tasks_map = {t["task_id"]: t for t in ds.tasks}

    for task in ds.tasks:
        session = sessions_map[task["session_id"]]
        assert session["start_time"] <= task["creation_time"]
        assert task["creation_time"] <= task["start_time"]
        assert task["start_time"] <= task["end_time"]
        assert task["end_time"] <= session["end_time"]

    for op in ds.operations:
        task = tasks_map[op["task_id"]]
        assert task["start_time"] <= op["start_time"]
        assert op["start_time"] <= op["end_time"]
        assert op["end_time"] <= task["end_time"]


def test_detection_coordinate_bounds():
    """Verify that all MongoDB detection bounding boxes and confidence scores are normalized in [0.0, 1.0]."""
    generator = SimulationGenerator(seed=42, scale="small")
    ds = generator.generate()

    for det in ds.detections:
        assert 0.0 <= det["confidence_score"] <= 1.0
        box = det["bounding_box"]
        assert 0.0 <= box["ymin"] <= 1.0
        assert 0.0 <= box["xmin"] <= 1.0
        assert 0.0 <= box["ymax"] <= 1.0
        assert 0.0 <= box["xmax"] <= 1.0
        assert box["ymin"] <= box["ymax"]
        assert box["xmin"] <= box["xmax"]


def test_safe_purge_requires_confirmation():
    """Verify that reset_simulated_data rejects purge requests without explicit confirmation."""
    with pytest.raises(ValueError, match="Purge aborted"):
        reset_simulated_data(confirm=False)


def test_all_relational_ids_fit_varchar_36():
    """Verify all primary and foreign key IDs fit within MySQL VARCHAR(36) constraints."""
    generator = SimulationGenerator(seed=42, scale="small")
    ds = generator.generate()
    for s in ds.sessions:
        assert len(s["session_id"]) <= 36
    for t in ds.tasks:
        assert len(t["task_id"]) <= 36
        assert len(t["session_id"]) <= 36
    for d in ds.decisions:
        assert len(d["decision_id"]) <= 36
        assert len(d["session_id"]) <= 36
        if d.get("task_id"):
            assert len(d["task_id"]) <= 36
    for o in ds.operations:
        assert len(o["operation_id"]) <= 36
        assert len(o["task_id"]) <= 36
        assert len(o["device_id"]) <= 36
    for e in ds.system_events:
        assert len(e["event_id"]) <= 36
        assert len(e["device_id"]) <= 36
        if e.get("operation_id"):
            assert len(e["operation_id"]) <= 36

