-- ==============================================================================
-- Post-Harvest DBMS Baseline Relational Schema (MySQL 8.4 LTS)
-- Project: Intelligent Data Management and Operational Analytics for
--          Autonomous Post-Harvest Material Handling Systems
-- Maintainer: Rakshith Raghavendra (Project Lead & Database Architect)
-- Reference: docs/database/MYSQL_DESIGN.md
-- ==============================================================================

-- Drop tables in reverse dependency order if reconstructing
DROP TABLE IF EXISTS system_event;
DROP TABLE IF EXISTS operation;
DROP TABLE IF EXISTS decision;
DROP TABLE IF EXISTS task;
DROP TABLE IF EXISTS device;
DROP TABLE IF EXISTS ai_model;
DROP TABLE IF EXISTS session;

-- ------------------------------------------------------------------------------
-- 1. Table: session
-- Operational sessions representing post-harvest grading/handling runs.
-- ------------------------------------------------------------------------------
CREATE TABLE session (
    session_id VARCHAR(36) NOT NULL,
    start_time DATETIME NOT NULL,
    end_time DATETIME NULL,
    environment VARCHAR(100) NOT NULL,
    session_status ENUM('INITIALIZING', 'ACTIVE', 'PAUSED', 'COMPLETED', 'ABORTED') NOT NULL DEFAULT 'INITIALIZING',
    notes TEXT NULL,
    provenance VARCHAR(20) NOT NULL DEFAULT 'SIMULATED',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (session_id),
    CONSTRAINT chk_session_times CHECK (end_time IS NULL OR end_time >= start_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_session_status ON session(session_status);
CREATE INDEX idx_session_start_time ON session(start_time);

-- ------------------------------------------------------------------------------
-- 2. Table: ai_model
-- Registry of object detection and classification models.
-- ------------------------------------------------------------------------------
CREATE TABLE ai_model (
    model_id VARCHAR(36) NOT NULL,
    model_name VARCHAR(100) NOT NULL,
    model_version VARCHAR(50) NOT NULL,
    configuration JSON NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    provenance VARCHAR(20) NOT NULL DEFAULT 'SIMULATED',
    PRIMARY KEY (model_id),
    CONSTRAINT uq_model_name_version UNIQUE (model_name, model_version)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------------------------
-- 3. Table: device
-- Registry of physical hardware equipment (cameras, robotic arms, AGVs).
-- ------------------------------------------------------------------------------
CREATE TABLE device (
    device_id VARCHAR(36) NOT NULL,
    device_name VARCHAR(100) NOT NULL,
    device_type VARCHAR(50) NOT NULL,
    device_status ENUM('ONLINE', 'OFFLINE', 'CALIBRATING', 'FAULT') NOT NULL DEFAULT 'ONLINE',
    description TEXT NULL,
    provenance VARCHAR(20) NOT NULL DEFAULT 'SIMULATED',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (device_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_device_type ON device(device_type);
CREATE INDEX idx_device_status ON device(device_status);

-- ------------------------------------------------------------------------------
-- 4. Table: task
-- Operational tasks spawned within a session (inspection, grading, pick-and-place).
-- Note: Accidental FK task_id self-reference removed per approved DEC-01.
-- ------------------------------------------------------------------------------
CREATE TABLE task (
    task_id VARCHAR(36) NOT NULL,
    session_id VARCHAR(36) NOT NULL,
    task_type VARCHAR(50) NOT NULL,
    target_description TEXT NULL,
    priority ENUM('LOW', 'MEDIUM', 'HIGH', 'CRITICAL') NOT NULL DEFAULT 'MEDIUM',
    creation_time DATETIME NOT NULL,
    start_time DATETIME NULL,
    end_time DATETIME NULL,
    task_status ENUM('PENDING', 'IN_PROGRESS', 'COMPLETED', 'FAILED', 'CANCELLED') NOT NULL DEFAULT 'PENDING',
    provenance VARCHAR(20) NOT NULL DEFAULT 'SIMULATED',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (task_id),
    CONSTRAINT fk_task_session FOREIGN KEY (session_id) REFERENCES session(session_id) ON DELETE CASCADE,
    CONSTRAINT chk_task_times CHECK (
        (start_time IS NULL OR start_time >= creation_time) AND
        (end_time IS NULL OR (start_time IS NOT NULL AND end_time >= start_time))
    )
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_task_session ON task(session_id);
CREATE INDEX idx_task_status ON task(task_status);
CREATE INDEX idx_task_priority ON task(priority);

-- ------------------------------------------------------------------------------
-- 5. Table: decision
-- Autonomous decision rationale and action selection.
-- Note: 'rescription' typo eliminated; 'rationale' maintained per approved DEC-02.
-- Note: task_id nullable per approved DEC-05.
-- ------------------------------------------------------------------------------
CREATE TABLE decision (
    decision_id VARCHAR(36) NOT NULL,
    session_id VARCHAR(36) NOT NULL,
    task_id VARCHAR(36) NULL,
    decision_time DATETIME NOT NULL,
    decision_type VARCHAR(50) NOT NULL,
    selected_action VARCHAR(100) NOT NULL,
    rationale TEXT NOT NULL,
    input_reference JSON NULL,
    provenance VARCHAR(20) NOT NULL DEFAULT 'SIMULATED',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (decision_id),
    CONSTRAINT fk_decision_session FOREIGN KEY (session_id) REFERENCES session(session_id) ON DELETE CASCADE,
    CONSTRAINT fk_decision_task FOREIGN KEY (task_id) REFERENCES task(task_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_decision_session ON decision(session_id);
CREATE INDEX idx_decision_task ON decision(task_id);
CREATE INDEX idx_decision_time ON decision(decision_time);

-- ------------------------------------------------------------------------------
-- 6. Table: operation
-- Physical actuation steps executed by robotic manipulators or AGVs.
-- Note: device_id FK included per approved DEC-03.
-- ------------------------------------------------------------------------------
CREATE TABLE operation (
    operation_id VARCHAR(36) NOT NULL,
    task_id VARCHAR(36) NOT NULL,
    device_id VARCHAR(36) NOT NULL,
    operation_type VARCHAR(50) NOT NULL,
    start_time DATETIME NOT NULL,
    end_time DATETIME NULL,
    operation_status ENUM('IN_PROGRESS', 'SUCCESS', 'FAILURE', 'TIMEOUT') NOT NULL DEFAULT 'IN_PROGRESS',
    result TEXT NULL,
    provenance VARCHAR(20) NOT NULL DEFAULT 'SIMULATED',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (operation_id),
    CONSTRAINT fk_op_task FOREIGN KEY (task_id) REFERENCES task(task_id) ON DELETE CASCADE,
    CONSTRAINT fk_op_device FOREIGN KEY (device_id) REFERENCES device(device_id) ON DELETE RESTRICT,
    CONSTRAINT chk_op_times CHECK (end_time IS NULL OR end_time >= start_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_op_task ON operation(task_id);
CREATE INDEX idx_op_device ON operation(device_id);
CREATE INDEX idx_op_status ON operation(operation_status);

-- ------------------------------------------------------------------------------
-- 7. Table: system_event
-- Structured operational status changes, warnings, and faults.
-- Note: operation_id nullable per approved DEC-05.
-- ------------------------------------------------------------------------------
CREATE TABLE system_event (
    event_id VARCHAR(36) NOT NULL,
    device_id VARCHAR(36) NOT NULL,
    operation_id VARCHAR(36) NULL,
    event_time DATETIME NOT NULL,
    event_type ENUM('INFO', 'WARNING', 'ERROR', 'CRITICAL_FAULT') NOT NULL DEFAULT 'INFO',
    description TEXT NOT NULL,
    resolution_status ENUM('OPEN', 'ACKNOWLEDGED', 'RESOLVED', 'IGNORED') NOT NULL DEFAULT 'OPEN',
    provenance VARCHAR(20) NOT NULL DEFAULT 'SIMULATED',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (event_id),
    CONSTRAINT fk_event_device FOREIGN KEY (device_id) REFERENCES device(device_id) ON DELETE RESTRICT,
    CONSTRAINT fk_event_op FOREIGN KEY (operation_id) REFERENCES operation(operation_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_event_device ON system_event(device_id);
CREATE INDEX idx_event_op ON system_event(operation_id);
CREATE INDEX idx_event_type ON system_event(event_type);
CREATE INDEX idx_event_status ON system_event(resolution_status);
CREATE INDEX idx_event_time ON system_event(event_time);

