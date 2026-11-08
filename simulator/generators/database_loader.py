"""Database ingestion and reset handler for simulated operational data."""

import logging
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from pymongo.database import Database

from backend.app.database.mysql import SessionLocal, check_mysql_connection
from backend.app.database.mongodb import get_mongo_db, check_mongodb_connection
from backend.app.models import (
    Device,
    AIModel,
    Session as SessionModel,
    Task as TaskModel,
    Decision as DecisionModel,
    Operation as OperationModel,
    SystemEvent as SystemEventModel,
)
from simulator.generators.data_generator import GeneratedDataset

logger = logging.getLogger(__name__)


def insert_dataset_into_databases(
    dataset: GeneratedDataset,
    db_session: Optional[Session] = None,
    mongo_db: Optional[Database] = None,
) -> Dict[str, Any]:
    """Persist generated dataset into MySQL and MongoDB.

    Maintains referential integrity order:
    1. Devices & AI Models (seeded/verified)
    2. Sessions
    3. Tasks
    4. Decisions
    5. Operations
    6. System Events
    7. MongoDB Detections
    8. MongoDB Telemetry Logs
    """
    records_inserted = {
        "devices": 0,
        "models": 0,
        "sessions": 0,
        "tasks": 0,
        "decisions": 0,
        "operations": 0,
        "system_events": 0,
        "detections": 0,
        "telemetry_logs": 0,
    }

    # Verify connection status
    mysql_online = check_mysql_connection()
    mongo_online = check_mongodb_connection()

    if not mysql_online:
        logger.warning("MySQL connection check failed. Skipping relational insertion.")
    else:
        close_session = False
        if db_session is None:
            db_session = SessionLocal()
            close_session = True

        try:
            # 1. Devices (insert or merge)
            for d_data in dataset.devices:
                existing = db_session.query(Device).filter_by(device_id=d_data["device_id"]).first()
                if not existing:
                    dev = Device(**d_data)
                    db_session.add(dev)
                    records_inserted["devices"] += 1

            # 2. Models
            for m_data in dataset.models:
                existing = db_session.query(AIModel).filter_by(model_id=m_data["model_id"]).first()
                if not existing:
                    model = AIModel(**m_data)
                    db_session.add(model)
                    records_inserted["models"] += 1

            db_session.commit()

            # 3. Sessions
            for s_data in dataset.sessions:
                existing = db_session.query(SessionModel).filter_by(session_id=s_data["session_id"]).first()
                if not existing:
                    s_obj = SessionModel(**s_data)
                    db_session.add(s_obj)
                    records_inserted["sessions"] += 1
            db_session.commit()

            # 4. Tasks
            for t_data in dataset.tasks:
                existing = db_session.query(TaskModel).filter_by(task_id=t_data["task_id"]).first()
                if not existing:
                    t_obj = TaskModel(**t_data)
                    db_session.add(t_obj)
                    records_inserted["tasks"] += 1
            db_session.commit()

            # 5. Decisions
            for dec_data in dataset.decisions:
                existing = db_session.query(DecisionModel).filter_by(decision_id=dec_data["decision_id"]).first()
                if not existing:
                    dec_obj = DecisionModel(**dec_data)
                    db_session.add(dec_obj)
                    records_inserted["decisions"] += 1
            db_session.commit()

            # 6. Operations
            for op_data in dataset.operations:
                existing = db_session.query(OperationModel).filter_by(operation_id=op_data["operation_id"]).first()
                if not existing:
                    op_obj = OperationModel(**op_data)
                    db_session.add(op_obj)
                    records_inserted["operations"] += 1
            db_session.commit()

            # 7. System Events
            for ev_data in dataset.system_events:
                existing = db_session.query(SystemEventModel).filter_by(event_id=ev_data["event_id"]).first()
                if not existing:
                    ev_obj = SystemEventModel(**ev_data)
                    db_session.add(ev_obj)
                    records_inserted["system_events"] += 1
            db_session.commit()

        except Exception as exc:
            db_session.rollback()
            logger.error("Error inserting relational records: %s", exc)
            raise
        finally:
            if close_session:
                db_session.close()

    # MongoDB Documents
    if not mongo_online:
        logger.warning("MongoDB connection check failed. Skipping document insertion.")
    else:
        if mongo_db is None:
            mongo_db = get_mongo_db()

        try:
            if dataset.detections:
                mongo_db["detections"].insert_many(dataset.detections, ordered=False)
                records_inserted["detections"] = len(dataset.detections)

            if dataset.telemetry_logs:
                mongo_db["telemetry_logs"].insert_many(dataset.telemetry_logs, ordered=False)
                records_inserted["telemetry_logs"] = len(dataset.telemetry_logs)
        except Exception as exc:
            logger.error("Error inserting MongoDB documents: %s", exc)
            raise

    return records_inserted


def reset_simulated_data(
    confirm: bool = False,
    db_session: Optional[Session] = None,
    mongo_db: Optional[Database] = None,
) -> Dict[str, int]:
    """Safely purge simulated records from MySQL and MongoDB.

    Requires explicit confirmation flag confirm=True.
    Only deletes records with provenance == 'SIMULATED'.
    """
    if not confirm:
        raise ValueError(
            "Purge aborted: resetting simulated data requires explicit confirmation (confirm=True)."
        )

    purged_counts = {
        "system_events": 0,
        "operations": 0,
        "decisions": 0,
        "tasks": 0,
        "sessions": 0,
        "detections": 0,
        "telemetry_logs": 0,
    }

    if check_mysql_connection():
        close_session = False
        if db_session is None:
            db_session = SessionLocal()
            close_session = True

        try:
            # Delete in reverse foreign key order
            purged_counts["system_events"] = (
                db_session.query(SystemEventModel).filter_by(provenance="SIMULATED").delete()
            )
            purged_counts["operations"] = (
                db_session.query(OperationModel).filter_by(provenance="SIMULATED").delete()
            )
            purged_counts["decisions"] = (
                db_session.query(DecisionModel).filter_by(provenance="SIMULATED").delete()
            )
            purged_counts["tasks"] = (
                db_session.query(TaskModel).filter_by(provenance="SIMULATED").delete()
            )
            purged_counts["sessions"] = (
                db_session.query(SessionModel).filter_by(provenance="SIMULATED").delete()
            )
            db_session.commit()
        except Exception as exc:
            db_session.rollback()
            logger.error("Failed to reset MySQL simulation data: %s", exc)
            raise
        finally:
            if close_session:
                db_session.close()

    if check_mongodb_connection():
        if mongo_db is None:
            mongo_db = get_mongo_db()
        try:
            res_det = mongo_db["detections"].delete_many({"provenance": "SIMULATED"})
            purged_counts["detections"] = res_det.deleted_count
            res_telem = mongo_db["telemetry_logs"].delete_many({"provenance": "SIMULATED"})
            purged_counts["telemetry_logs"] = res_telem.deleted_count
        except Exception as exc:
            logger.error("Failed to reset MongoDB simulation data: %s", exc)
            raise

    return purged_counts
