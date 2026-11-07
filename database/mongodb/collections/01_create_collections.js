// ==============================================================================
// MongoDB Collection Setup Script (MongoDB 8.0 Community)
// Project: Intelligent Data Management and Operational Analytics for
//          Autonomous Post-Harvest Material Handling Systems
// Reference: docs/database/MONGODB_DESIGN.md
// ==============================================================================

const dbName = "post_harvest_telemetry";
const db = db.getSiblingDB(dbName);

print("Initializing MongoDB collections for " + dbName + "...");

// ------------------------------------------------------------------------------
// 1. Collection: detections
// Stores vision detection coordinates, confidence scores, and frame references.
// ------------------------------------------------------------------------------
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
        detection_id: {
          bsonType: "string",
          description: "Unique string UUID identifier for the detection observation"
        },
        session_id: {
          bsonType: "string",
          description: "Foreign reference to MySQL session.session_id"
        },
        model_id: {
          bsonType: "string",
          description: "Foreign reference to MySQL ai_model.model_id"
        },
        device_id: {
          bsonType: "string",
          description: "Foreign reference to MySQL device.device_id"
        },
        detection_time: {
          bsonType: "date",
          description: "Timestamp when the image frame was captured and processed"
        },
        class_label: {
          bsonType: "string",
          description: "Produce classification label (e.g. GRADE_A_APPLE, BLEMISHED)"
        },
        confidence_score: {
          bsonType: "double",
          minimum: 0.0,
          maximum: 1.0,
          description: "Model prediction confidence normalized between 0.0 and 1.0"
        },
        bounding_box: {
          bsonType: "object",
          required: ["ymin", "xmin", "ymax", "xmax"],
          properties: {
            ymin: { bsonType: "double" },
            xmin: { bsonType: "double" },
            ymax: { bsonType: "double" },
            xmax: { bsonType: "double" }
          },
          description: "Normalized 2D bounding box coordinates [0.0, 1.0]"
        },
        frame_reference: {
          bsonType: "string",
          description: "Identifier or filename reference for the source frame"
        },
        extra_metadata: {
          bsonType: "object",
          description: "Optional dictionary containing defect metrics or sizing"
        },
        provenance: {
          bsonType: "string",
          enum: ["SIMULATED", "MANUAL_TEST"],
          description: "Explicit provenance indicator"
        },
        created_at: {
          bsonType: "date",
          description: "Persistence timestamp"
        }
      }
    }
  }
});

// ------------------------------------------------------------------------------
// 2. Collection: telemetry_logs
// Stores high-frequency hardware health metrics, AGV currents, IMU orientations.
// ------------------------------------------------------------------------------
db.createCollection("telemetry_logs", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: [
        "telemetry_id",
        "device_id",
        "session_id",
        "timestamp",
        "metrics",
        "provenance"
      ],
      properties: {
        telemetry_id: {
          bsonType: "string",
          description: "Unique string UUID identifier for the telemetry entry"
        },
        device_id: {
          bsonType: "string",
          description: "Foreign reference to MySQL device.device_id"
        },
        session_id: {
          bsonType: "string",
          description: "Foreign reference to MySQL session.session_id"
        },
        timestamp: {
          bsonType: "date",
          description: "High-resolution metric capture timestamp"
        },
        metrics: {
          bsonType: "object",
          description: "Key-value metrics (e.g. motor currents, velocities, battery)"
        },
        provenance: {
          bsonType: "string",
          enum: ["SIMULATED", "MANUAL_TEST"],
          description: "Explicit provenance indicator"
        },
        created_at: {
          bsonType: "date",
          description: "Persistence timestamp"
        }
      }
    }
  }
});

print("Collections created successfully.");

