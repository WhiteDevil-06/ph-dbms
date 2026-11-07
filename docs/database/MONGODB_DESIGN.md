# MongoDB Document Database Design Specification (MongoDB 8.0 Community)
**Owner**: Rahul (Backend and Database Integration Developer) & Rakshith Raghavendra (Architect)

---

## 1. Overview
In accordance with DFD Level 1/2 and the Data Ownership Matrix, MongoDB is the authoritative repository for vision detection observations and unstructured/high-frequency telemetry streams.

Database name: `post_harvest_telemetry`

---

## 2. Collections and Document Schemas

### 2.1 Collection: `detections`
Authoritative store for computer vision detections, object localization bounding boxes, and produce classification scores.

#### Sample Document:
```json
{
  "_id": { "$oid": "672922ef1c4e2b001a123456" },
  "detection_id": "det-a1b2c3d4-e5f6-7890",
  "session_id": "sess-9876-abcd-ef01",
  "model_id": "model-yolov8-grading-v2",
  "device_id": "dev-cam-rgb-overhead-01",
  "detection_time": "2026-11-04T10:15:30.123Z",
  "class_label": "GRADE_A_APPLE",
  "confidence_score": 0.942,
  "bounding_box": {
    "ymin": 0.124,
    "xmin": 0.352,
    "ymax": 0.456,
    "xmax": 0.681
  },
  "frame_reference": "frame_20261104_101530_123.jpg",
  "extra_metadata": {
    "estimated_diameter_mm": 74.5,
    "surface_defect_percentage": 1.2,
    "lighting_condition_lux": 850
  },
  "provenance": "SIMULATED",
  "created_at": "2026-11-04T10:15:30.150Z"
}
```

#### JSON Schema Validator:
```javascript
db.createCollection("detections", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: [
        "detection_id",
        "session_id",
        "model_id",
        "device_id",
        "detection_time",
        "class_label",
        "confidence_score",
        "bounding_box",
        "frame_reference",
        "provenance"
      ],
      properties: {
        detection_id: { bsonType: "string" },
        session_id: { bsonType: "string" },
        model_id: { bsonType: "string" },
        device_id: { bsonType: "string" },
        detection_time: { bsonType: "date" },
        class_label: { bsonType: "string" },
        confidence_score: {
          bsonType: "double",
          minimum: 0.0,
          maximum: 1.0
        },
        bounding_box: {
          bsonType: "object",
          required: ["ymin", "xmin", "ymax", "xmax"],
          properties: {
            ymin: { bsonType: "double" },
            xmin: { bsonType: "double" },
            ymax: { bsonType: "double" },
            xmax: { bsonType: "double" }
          }
        },
        frame_reference: { bsonType: "string" },
        provenance: {
          bsonType: "string",
          enum: ["SIMULATED", "MANUAL_TEST"]
        }
      }
    }
  }
});
```

#### Indexes:
```javascript
db.detections.createIndex({ detection_id: 1 }, { unique: true });
db.detections.createIndex({ session_id: 1, detection_time: -1 });
db.detections.createIndex({ class_label: 1 });
db.detections.createIndex({ confidence_score: -1 });
db.detections.createIndex({ device_id: 1 });
```

---

### 2.2 Collection: `telemetry_logs`
High-frequency sensor outputs, AGV motor currents, and hardware health metrics.

#### Sample Document:
```json
{
  "_id": { "$oid": "672922ef1c4e2b001a999888" },
  "telemetry_id": "telem-5544-3322-1100",
  "device_id": "dev-agv-chassis-01",
  "session_id": "sess-9876-abcd-ef01",
  "timestamp": "2026-11-04T10:15:30.500Z",
  "metrics": {
    "battery_soc_percent": 88.5,
    "battery_voltage_v": 24.2,
    "motor_current_a": [1.4, 1.5, 1.3, 1.4],
    "chassis_linear_velocity_mps": 0.45,
    "imu_orientation_euler": { "roll": 0.2, "pitch": -0.1, "yaw": 45.6 }
  },
  "provenance": "SIMULATED",
  "created_at": "2026-11-04T10:15:30.510Z"
}
```

#### Indexes:
```javascript
db.telemetry_logs.createIndex({ telemetry_id: 1 }, { unique: true });
db.telemetry_logs.createIndex({ session_id: 1, timestamp: -1 });
db.telemetry_logs.createIndex({ device_id: 1, timestamp: -1 });
```

