"""Tests for SQLAlchemy ORM models and schema alignment."""

from datetime import datetime, timezone
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.app.database.base import Base
from backend.app.models import (
    Session,
    AIModel,
    Device,
    Task,
    Decision,
    Operation,
    SystemEvent,
    SessionStatus,
    DeviceStatus,
    TaskPriority,
    TaskStatus,
    OperationStatus,
    EventType,
    ResolutionStatus,
    DataProvenance,
)


@pytest.fixture
def in_memory_db():
    """Create an in-memory SQLite database for verifying schema integrity."""
    test_engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(bind=test_engine)
    TestingSession = sessionmaker(bind=test_engine)
    session = TestingSession()
    try:
        yield session
    finally:
        session.close()


def test_table_names():
    """Verify that ORM table names match baseline MySQL schema tables."""
    expected_tables = {
        "session",
        "ai_model",
        "device",
        "task",
        "decision",
        "operation",
        "system_event",
    }
    assert expected_tables.issubset(set(Base.metadata.tables.keys()))


def test_create_and_query_entities(in_memory_db):
    """Verify entity persistence, relationships, and constraints in-memory."""
    now = datetime(2026, 11, 4, 10, 0, 0)

    # 1. Device
    device = Device(
        device_id="dev-arm-01",
        device_name="Delta Sorter",
        device_type="ROBOTIC_ARM",
        device_status=DeviceStatus.ONLINE,
        description="4-DOF delta sorting manipulator",
        provenance=DataProvenance.SIMULATED.value,
        created_at=now,
    )
    in_memory_db.add(device)

    # 2. AI Model
    model = AIModel(
        model_id="model-yolo-01",
        model_name="YOLOv8 Produce",
        model_version="1.0.0",
        configuration={"classes": ["GRADE_A_APPLE", "GRADE_B_APPLE"]},
        provenance=DataProvenance.SIMULATED.value,
        created_at=now,
    )
    in_memory_db.add(model)

    # 3. Session
    session = Session(
        session_id="sess-001",
        start_time=now,
        end_time=datetime(2026, 11, 4, 11, 0, 0),
        environment="Packhouse Bay 1",
        session_status=SessionStatus.ACTIVE,
        notes="Automated grading run",
        provenance=DataProvenance.SIMULATED.value,
        created_at=now,
        updated_at=now,
    )
    in_memory_db.add(session)
    in_memory_db.flush()

    # 4. Task
    task = Task(
        task_id="tsk-001",
        session_id=session.session_id,
        task_type="GRADING",
        target_description="Tray 1 Apple sorting",
        priority=TaskPriority.HIGH,
        creation_time=now,
        start_time=now,
        end_time=datetime(2026, 11, 4, 10, 15, 0),
        task_status=TaskStatus.IN_PROGRESS,
        provenance=DataProvenance.SIMULATED.value,
        created_at=now,
        updated_at=now,
    )
    in_memory_db.add(task)
    in_memory_db.flush()

    # 5. Decision
    decision = Decision(
        decision_id="dec-001",
        session_id=session.session_id,
        task_id=task.task_id,
        decision_time=now,
        decision_type="GRADING",
        selected_action="ROUTE_GRADE_A",
        rationale="Surface defect area < 1%",
        input_reference={"detection_id": "det-123"},
        provenance=DataProvenance.SIMULATED.value,
        created_at=now,
    )
    in_memory_db.add(decision)

    # 6. Operation
    operation = Operation(
        operation_id="op-001",
        task_id=task.task_id,
        device_id=device.device_id,
        operation_type="GRASP",
        start_time=now,
        end_time=datetime(2026, 11, 4, 10, 1, 0),
        operation_status=OperationStatus.SUCCESS,
        result="Grasp confirmed by vacuum sensor",
        provenance=DataProvenance.SIMULATED.value,
        created_at=now,
        updated_at=now,
    )
    in_memory_db.add(operation)
    in_memory_db.flush()

    # 7. System Event
    event = SystemEvent(
        event_id="evt-001",
        device_id=device.device_id,
        operation_id=operation.operation_id,
        event_time=now,
        event_type=EventType.INFO,
        description="Routine grasp cycle executed successfully",
        resolution_status=ResolutionStatus.RESOLVED,
        provenance=DataProvenance.SIMULATED.value,
        created_at=now,
        updated_at=now,
    )
    in_memory_db.add(event)
    in_memory_db.commit()

    # Query checks & relationship traversal
    queried_session = in_memory_db.query(Session).filter_by(session_id="sess-001").one()
    assert len(queried_session.tasks) == 1
    assert queried_session.tasks[0].task_id == "tsk-001"
    assert len(queried_session.decisions) == 1
    assert queried_session.decisions[0].rationale == "Surface defect area < 1%"

    queried_task = queried_session.tasks[0]
    assert len(queried_task.operations) == 1
    assert queried_task.operations[0].operation_id == "op-001"
    assert queried_task.operations[0].device.device_id == "dev-arm-01"

    queried_device = in_memory_db.query(Device).filter_by(device_id="dev-arm-01").one()
    assert len(queried_device.operations) == 1
    assert len(queried_device.system_events) == 1
    assert queried_device.system_events[0].event_id == "evt-001"
