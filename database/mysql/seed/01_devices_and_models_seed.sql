-- ==============================================================================
-- Post-Harvest DBMS Baseline Seed Data (MySQL 8.4 LTS)
-- Project: Intelligent Data Management and Operational Analytics for
--          Autonomous Post-Harvest Material Handling Systems
-- Maintainer: Rakshith Raghavendra (Project Lead & Database Architect)
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- Seed Equipment / Devices
-- ------------------------------------------------------------------------------
INSERT INTO device (device_id, device_name, device_type, device_status, description, provenance) VALUES
('dev-cam-rgb-01', 'Overhead Inspection Camera A1', 'RGB_CAMERA', 'ONLINE', 'High-resolution industrial camera mounted above grading conveyor line 1.', 'SIMULATED'),
('dev-cam-depth-01', 'Produce Depth Sensor D1', 'DEPTH_SENSOR', 'ONLINE', 'Structured-light 3D camera for produce volume estimation and grasp planning.', 'SIMULATED'),
('dev-arm-robotic-01', 'Delta Sorting Manipulator M1', 'ROBOTIC_ARM', 'ONLINE', '4-DOF high-speed parallel manipulator equipped with soft vacuum gripper.', 'SIMULATED'),
('dev-agv-chassis-01', 'Field Bin Transport AGV T1', 'AGV_CHASSIS', 'ONLINE', 'Autonomous mobile robotic base for transporting sorted produce crates to storage.', 'SIMULATED');

-- ------------------------------------------------------------------------------
-- Seed AI Models
-- ------------------------------------------------------------------------------
INSERT INTO ai_model (model_id, model_name, model_version, configuration, provenance) VALUES
('model-yolov8-grading-v1', 'YOLOv8 Produce Grading', '1.0.0', '{"input_resolution": [640, 640], "confidence_threshold": 0.65, "classes": ["GRADE_A_APPLE", "GRADE_B_APPLE", "REJECT_APPLE"]}', 'SIMULATED'),
('model-defect-detect-v2', 'ResNet Surface Defect Classifier', '2.1.0', '{"input_resolution": [224, 224], "defect_types": ["BRUISE", "PUNCTURE", "SCAB", "SUNBURN"]}', 'SIMULATED');

