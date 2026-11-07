// ==============================================================================
// MongoDB Index Setup Script (MongoDB 8.0 Community)
// Project: Intelligent Data Management and Operational Analytics for
//          Autonomous Post-Harvest Material Handling Systems
// Reference: docs/database/MONGODB_DESIGN.md
// ==============================================================================

const dbName = "post_harvest_telemetry";
const db = db.getSiblingDB(dbName);

print("Creating indexes for " + dbName + "...");

// Indexes for detections collection
db.detections.createIndex({ detection_id: 1 }, { unique: true, name: "idx_detection_id_unique" });
db.detections.createIndex({ session_id: 1, detection_time: -1 }, { name: "idx_session_time" });
db.detections.createIndex({ class_label: 1 }, { name: "idx_class_label" });
db.detections.createIndex({ confidence_score: -1 }, { name: "idx_confidence" });
db.detections.createIndex({ device_id: 1 }, { name: "idx_device_id" });

// Indexes for telemetry_logs collection
db.telemetry_logs.createIndex({ telemetry_id: 1 }, { unique: true, name: "idx_telemetry_id_unique" });
db.telemetry_logs.createIndex({ session_id: 1, timestamp: -1 }, { name: "idx_telemetry_session_time" });
db.telemetry_logs.createIndex({ device_id: 1, timestamp: -1 }, { name: "idx_telemetry_device_time" });

print("Indexes created successfully.");

