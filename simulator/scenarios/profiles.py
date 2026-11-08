"""Simulation Scale Profiles and Hardware/Produce Catalogs."""

from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass(frozen=True)
class ScaleProfile:
    name: str
    target_sessions: int
    tasks_per_session: int
    detections_per_session: int
    ops_per_task: int
    events_per_session: int


SCALE_PROFILES: Dict[str, ScaleProfile] = {
    "small": ScaleProfile(
        name="small",
        target_sessions=1,
        tasks_per_session=5,
        detections_per_session=20,
        ops_per_task=2,
        events_per_session=2,
    ),
    "medium": ScaleProfile(
        name="medium",
        target_sessions=5,
        tasks_per_session=10,
        detections_per_session=100,
        ops_per_task=2,
        events_per_session=4,
    ),
    "demo": ScaleProfile(
        name="demo",
        target_sessions=10,
        tasks_per_session=12,
        detections_per_session=350,
        ops_per_task=3,
        events_per_session=10,
    ),
}

# Seeded Baseline Devices (matching 01_devices_and_models_seed.sql)
DEFAULT_DEVICES: List[Dict[str, Any]] = [
    {
        "device_id": "dev-cam-rgb-01",
        "device_name": "Overhead Inspection Camera A1",
        "device_type": "RGB_CAMERA",
        "device_status": "ONLINE",
        "description": "High-resolution industrial camera mounted above grading conveyor line 1.",
        "provenance": "SIMULATED",
    },
    {
        "device_id": "dev-cam-depth-01",
        "device_name": "Produce Depth Sensor D1",
        "device_type": "DEPTH_SENSOR",
        "device_status": "ONLINE",
        "description": "Structured-light 3D camera for produce volume estimation and grasp planning.",
        "provenance": "SIMULATED",
    },
    {
        "device_id": "dev-arm-robotic-01",
        "device_name": "Delta Sorting Manipulator M1",
        "device_type": "ROBOTIC_ARM",
        "device_status": "ONLINE",
        "description": "4-DOF high-speed parallel manipulator equipped with soft vacuum gripper.",
        "provenance": "SIMULATED",
    },
    {
        "device_id": "dev-agv-chassis-01",
        "device_name": "Field Bin Transport AGV T1",
        "device_type": "AGV_CHASSIS",
        "device_status": "ONLINE",
        "description": "Autonomous mobile robotic base for transporting sorted produce crates to storage.",
        "provenance": "SIMULATED",
    },
]

# Seeded Baseline AI Models (matching 01_devices_and_models_seed.sql)
DEFAULT_MODELS: List[Dict[str, Any]] = [
    {
        "model_id": "model-yolov8-grading-v1",
        "model_name": "YOLOv8 Produce Grading",
        "model_version": "1.0.0",
        "configuration": {
            "input_resolution": [640, 640],
            "confidence_threshold": 0.65,
            "classes": ["GRADE_A_APPLE", "GRADE_B_APPLE", "REJECT_APPLE", "BLEMISHED_APPLE"],
        },
        "provenance": "SIMULATED",
    },
    {
        "model_id": "model-defect-detect-v2",
        "model_name": "ResNet Surface Defect Classifier",
        "model_version": "2.1.0",
        "configuration": {
            "input_resolution": [224, 224],
            "defect_types": ["BRUISE", "PUNCTURE", "SCAB", "SUNBURN"],
        },
        "provenance": "SIMULATED",
    },
]

ENVIRONMENTS: List[str] = [
    "Packhouse Sorting Bay 1",
    "Packhouse Sorting Bay 2",
    "Cold Storage Dispatch Bay",
    "Pre-Grading Conveyor Belt 3",
    "Produce Washing & Drying Cell",
]

PRODUCE_CLASSES: List[str] = [
    "GRADE_A_APPLE",
    "GRADE_B_APPLE",
    "BLEMISHED_APPLE",
    "REJECT_APPLE",
    "GRADE_A_CITRUS",
    "GRADE_B_CITRUS",
]

TASK_TYPES: List[str] = [
    "CONVEYOR_INSPECTION",
    "QUALITY_GRADING",
    "BIN_PICK_AND_PLACE",
    "CRATE_TRANSPORT",
]

OPERATION_TYPES: List[str] = [
    "VISION_CAPTURE",
    "GRASP",
    "LIFT",
    "TRANSPORT",
    "RELEASE",
    "CRATE_TRANSFER",
]
