"""Deterministic Synthetic Operational Data Generator for Post-Harvest DBMS.

Implements plausible operational sessions, tasks, detections, decisions, operations,
system events, and telemetry logs adhering to SIMULATION_SPEC.md.
"""

import random
import uuid
from datetime import datetime, timedelta, timezone
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

from simulator.scenarios.profiles import (
    SCALE_PROFILES,
    ScaleProfile,
    DEFAULT_DEVICES,
    DEFAULT_MODELS,
    ENVIRONMENTS,
    PRODUCE_CLASSES,
    TASK_TYPES,
    OPERATION_TYPES,
)


@dataclass
class GeneratedDataset:
    seed: int
    scale: str
    devices: List[Dict[str, Any]] = field(default_factory=list)
    models: List[Dict[str, Any]] = field(default_factory=list)
    sessions: List[Dict[str, Any]] = field(default_factory=list)
    tasks: List[Dict[str, Any]] = field(default_factory=list)
    decisions: List[Dict[str, Any]] = field(default_factory=list)
    operations: List[Dict[str, Any]] = field(default_factory=list)
    system_events: List[Dict[str, Any]] = field(default_factory=list)
    detections: List[Dict[str, Any]] = field(default_factory=list)
    telemetry_logs: List[Dict[str, Any]] = field(default_factory=list)

    @property
    def counts(self) -> Dict[str, int]:
        return {
            "devices": len(self.devices),
            "models": len(self.models),
            "sessions": len(self.sessions),
            "tasks": len(self.tasks),
            "decisions": len(self.decisions),
            "operations": len(self.operations),
            "system_events": len(self.system_events),
            "detections": len(self.detections),
            "telemetry_logs": len(self.telemetry_logs),
        }


class SimulationGenerator:
    """Deterministic simulation generator using an isolated random.Random instance."""

    def __init__(self, seed: int = 42, scale: str = "demo"):
        self.seed = seed
        self.scale = scale
        self.rng = random.Random(seed)
        self.profile: ScaleProfile = SCALE_PROFILES.get(scale, SCALE_PROFILES["demo"])

    def _generate_uuid(self, prefix: str) -> str:
        """Generate deterministic UUID based on seed progression."""
        raw_hex = f"{self.rng.getrandbits(128):032x}"
        formatted = f"{raw_hex[:8]}-{raw_hex[8:12]}-{raw_hex[12:16]}-{raw_hex[16:20]}-{raw_hex[20:32]}"
        return f"{prefix}-{formatted}"

    def generate(self) -> GeneratedDataset:
        """Synthesize all post-harvest relational and document datasets."""
        dataset = GeneratedDataset(seed=self.seed, scale=self.scale)

        # 1. Baseline Devices and AI Models
        dataset.devices = [dict(d) for d in DEFAULT_DEVICES]
        dataset.models = [dict(m) for m in DEFAULT_MODELS]

        camera_devices = [d["device_id"] for d in dataset.devices if "cam" in d["device_id"]]
        manipulator_devices = [d["device_id"] for d in dataset.devices if "arm" in d["device_id"]]
        agv_devices = [d["device_id"] for d in dataset.devices if "agv" in d["device_id"]]
        grading_model = dataset.models[0]["model_id"]
        defect_model = dataset.models[1]["model_id"]

        # Base chronological starting time
        base_time = datetime(2026, 11, 4, 8, 0, 0)

        # 2. Generate Sessions
        for s_idx in range(self.profile.target_sessions):
            session_id = self._generate_uuid("sess")
            session_start = base_time + timedelta(hours=s_idx * 2, minutes=self.rng.randint(0, 15))
            session_env = self.rng.choice(ENVIRONMENTS)

            # Plausible Session Duration (30 to 75 minutes)
            session_duration_minutes = self.rng.randint(35, 75)
            session_end = session_start + timedelta(minutes=session_duration_minutes)

            # Session Status (most completed, rare aborted)
            is_aborted = self.rng.random() < 0.08
            session_status = "ABORTED" if is_aborted else "COMPLETED"

            session_record = {
                "session_id": session_id,
                "start_time": session_start,
                "end_time": session_end,
                "environment": session_env,
                "session_status": session_status,
                "notes": f"Simulated autonomous run in {session_env} with profile {self.scale}.",
                "provenance": "SIMULATED",
                "created_at": session_start,
                "updated_at": session_end,
            }
            dataset.sessions.append(session_record)

            # 3. Tasks per Session
            task_interval_sec = int((session_duration_minutes * 60 - 120) / max(1, self.profile.tasks_per_session))
            curr_time = session_start + timedelta(seconds=60)

            for t_idx in range(self.profile.tasks_per_session):
                task_id = self._generate_uuid("tsk")
                task_creation = curr_time
                task_start = task_creation + timedelta(seconds=self.rng.randint(2, 10))
                task_type = self.rng.choice(TASK_TYPES)

                # Estimated task execution length (60 to 180 seconds)
                task_length_sec = min(task_interval_sec - 15, self.rng.randint(60, 180))
                task_end = task_start + timedelta(seconds=task_length_sec)

                # Error rate for tasks (~8%)
                is_task_failed = self.rng.random() < 0.08
                task_status = "FAILED" if is_task_failed else "COMPLETED"

                task_priority = self.rng.choice(["LOW", "MEDIUM", "HIGH", "CRITICAL"])
                target_desc = f"Batch inspection/sorting for tray #{s_idx * 10 + t_idx + 1}"

                task_record = {
                    "task_id": task_id,
                    "session_id": session_id,
                    "task_type": task_type,
                    "target_description": target_desc,
                    "priority": task_priority,
                    "creation_time": task_creation,
                    "start_time": task_start,
                    "end_time": task_end,
                    "task_status": task_status,
                    "provenance": "SIMULATED",
                    "created_at": task_creation,
                    "updated_at": task_end,
                }
                dataset.tasks.append(task_record)

                # 4. Detections associated with Task & Session
                detections_for_task = max(2, int(self.profile.detections_per_session / self.profile.tasks_per_session))
                cam_device = self.rng.choice(camera_devices) if camera_devices else "dev-cam-rgb-01"

                task_detections = []
                for d_idx in range(detections_for_task):
                    detection_id = self._generate_uuid("det")
                    det_time = task_start + timedelta(seconds=d_idx * 4 + self.rng.uniform(0.1, 1.5))
                    produce_class = self.rng.choice(PRODUCE_CLASSES)

                    # Realistic confidence score: mostly 0.82 - 0.99, occasionally < 0.70 (Scenario B)
                    is_low_confidence = self.rng.random() < 0.10
                    if is_low_confidence:
                        confidence = round(self.rng.uniform(0.48, 0.68), 3)
                    else:
                        confidence = round(self.rng.uniform(0.82, 0.985), 3)

                    # Bounding box normalized coordinates [0.0, 1.0]
                    xmin = round(self.rng.uniform(0.05, 0.65), 3)
                    ymin = round(self.rng.uniform(0.05, 0.65), 3)
                    box_w = round(self.rng.uniform(0.12, 0.28), 3)
                    box_h = round(self.rng.uniform(0.12, 0.28), 3)
                    xmax = min(1.0, round(xmin + box_w, 3))
                    ymax = min(1.0, round(ymin + box_h, 3))

                    frame_ref = f"frame_{det_time.strftime('%Y%m%d_%H%M%S')}_{d_idx:02d}.jpg"

                    detection_doc = {
                        "detection_id": detection_id,
                        "session_id": session_id,
                        "model_id": grading_model if "GRADE" in produce_class else defect_model,
                        "device_id": cam_device,
                        "detection_time": det_time,
                        "class_label": produce_class,
                        "confidence_score": confidence,
                        "bounding_box": {
                            "ymin": ymin,
                            "xmin": xmin,
                            "ymax": ymax,
                            "xmax": xmax,
                        },
                        "frame_reference": frame_ref,
                        "extra_metadata": {
                            "estimated_diameter_mm": round(self.rng.uniform(65.0, 88.0), 1),
                            "surface_defect_percentage": round(self.rng.uniform(0.0, 4.5), 2),
                            "lighting_condition_lux": self.rng.randint(750, 950),
                        },
                        "provenance": "SIMULATED",
                        "created_at": det_time,
                    }
                    dataset.detections.append(detection_doc)
                    task_detections.append(detection_doc)

                # 5. Autonomous Decision per Task
                decision_id = self._generate_uuid("dec")
                dec_time = task_start + timedelta(seconds=int(task_length_sec * 0.35))
                primary_det = task_detections[0]

                if primary_det["confidence_score"] < 0.70:
                    dec_type = "REINSPECTION"
                    action = "REINSPECT_PRODUCE"
                    rationale = (
                        f"Confidence {primary_det['confidence_score']} below threshold 0.70; "
                        f"produce orientation ambiguous. Secondary verification scheduled."
                    )
                elif "REJECT" in primary_det["class_label"] or "BLEMISHED" in primary_det["class_label"]:
                    dec_type = "DISCARD"
                    action = "ROUTE_TO_REJECT_BIN"
                    rationale = (
                        f"Defect area detected: {primary_det['extra_metadata']['surface_defect_percentage']}%. "
                        f"Classified as {primary_det['class_label']}."
                    )
                else:
                    dec_type = "GRADING"
                    action = "ROUTE_TO_GRADE_A_BIN" if "GRADE_A" in primary_det["class_label"] else "ROUTE_TO_GRADE_B_BIN"
                    rationale = (
                        f"High confidence {primary_det['confidence_score']} produce verified. "
                        f"Diameter {primary_det['extra_metadata']['estimated_diameter_mm']}mm meets grade criteria."
                    )

                decision_record = {
                    "decision_id": decision_id,
                    "session_id": session_id,
                    "task_id": task_id,
                    "decision_time": dec_time,
                    "decision_type": dec_type,
                    "selected_action": action,
                    "rationale": rationale,
                    "input_reference": {
                        "primary_detection_id": primary_det["detection_id"],
                        "confidence": primary_det["confidence_score"],
                        "class": primary_det["class_label"],
                    },
                    "provenance": "SIMULATED",
                    "created_at": dec_time,
                }
                dataset.decisions.append(decision_record)

                # 6. Operations per Task
                op_device = self.rng.choice(manipulator_devices) if manipulator_devices else "dev-arm-robotic-01"
                op_start_cursor = dec_time + timedelta(seconds=2)
                op_slice_sec = int((task_end - op_start_cursor).total_seconds() / max(1, self.profile.ops_per_task))

                for o_idx in range(self.profile.ops_per_task):
                    op_id = self._generate_uuid("op")
                    op_start = op_start_cursor + timedelta(seconds=o_idx * op_slice_sec)
                    op_duration = max(3, int(op_slice_sec * 0.85))
                    op_end = op_start + timedelta(seconds=op_duration)
                    op_type = OPERATION_TYPES[(o_idx + 1) % len(OPERATION_TYPES)]

                    # Realistic Failure rate for operations (~6-10%)
                    is_op_failed = is_task_failed and (o_idx == self.profile.ops_per_task - 1)
                    if is_op_failed:
                        op_status = self.rng.choice(["FAILURE", "TIMEOUT"])
                        op_result = "GRIPPER_VACUUM_LOSS: Suction pressure dropped below safe threshold during lift."
                    else:
                        op_status = "SUCCESS"
                        op_result = f"Operation {op_type} executed within nominal kinematic limits."

                    op_record = {
                        "operation_id": op_id,
                        "task_id": task_id,
                        "device_id": op_device,
                        "operation_type": op_type,
                        "start_time": op_start,
                        "end_time": op_end,
                        "operation_status": op_status,
                        "result": op_result,
                        "provenance": "SIMULATED",
                        "created_at": op_start,
                        "updated_at": op_end,
                    }
                    dataset.operations.append(op_record)

                    # Scenario C: Gripper Slip / Hardware Fault Event
                    if is_op_failed:
                        evt_id = self._generate_uuid("evt")
                        evt_record = {
                            "event_id": evt_id,
                            "device_id": op_device,
                            "operation_id": op_id,
                            "event_time": op_end,
                            "event_type": "WARNING" if op_status == "TIMEOUT" else "ERROR",
                            "description": f"Hardware anomaly during {op_type}: {op_result}",
                            "resolution_status": "OPEN",
                            "provenance": "SIMULATED",
                            "created_at": op_end,
                            "updated_at": op_end,
                        }
                        dataset.system_events.append(evt_record)

                # High-frequency AGV/Sensor Telemetry per Task
                telemetry_id = self._generate_uuid("telem")
                agv_device = self.rng.choice(agv_devices) if agv_devices else "dev-agv-chassis-01"
                telem_doc = {
                    "telemetry_id": telemetry_id,
                    "device_id": agv_device,
                    "session_id": session_id,
                    "timestamp": task_start,
                    "metrics": {
                        "battery_soc_percent": round(self.rng.uniform(70.0, 98.0), 1),
                        "battery_voltage_v": round(self.rng.uniform(23.8, 25.4), 2),
                        "motor_current_a": [
                            round(self.rng.uniform(1.1, 1.8), 2) for _ in range(4)
                        ],
                        "chassis_linear_velocity_mps": round(self.rng.uniform(0.15, 0.65), 2),
                        "imu_orientation_euler": {
                            "roll": round(self.rng.uniform(-0.5, 0.5), 2),
                            "pitch": round(self.rng.uniform(-0.5, 0.5), 2),
                            "yaw": round(self.rng.uniform(0.0, 360.0), 1),
                        },
                    },
                    "provenance": "SIMULATED",
                    "created_at": task_start,
                }
                dataset.telemetry_logs.append(telem_doc)

                curr_time = task_end + timedelta(seconds=15)

            # Plausible Session-Level Informational Events
            session_events_target = max(1, self.profile.events_per_session - len([e for e in dataset.system_events if any(op["operation_id"] == e.get("operation_id") for op in dataset.operations if op["task_id"] in [t["task_id"] for t in dataset.tasks if t["session_id"] == session_id])]))
            for ev_idx in range(session_events_target):
                dataset.system_events.append({
                    "event_id": self._generate_uuid("evt"),
                    "device_id": self.rng.choice(camera_devices) if camera_devices else "dev-cam-rgb-01",
                    "operation_id": None,
                    "event_time": session_start + timedelta(minutes=ev_idx * 15 + 5),
                    "event_type": "INFO",
                    "description": f"Periodic auto-calibration routine completed nominally for camera unit.",
                    "resolution_status": "RESOLVED",
                    "provenance": "SIMULATED",
                    "created_at": session_start + timedelta(minutes=ev_idx * 15 + 5),
                    "updated_at": session_start + timedelta(minutes=ev_idx * 15 + 5),
                })

        return dataset
