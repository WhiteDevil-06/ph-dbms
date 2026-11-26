-- ==============================================================================
-- Migration 02: JWT Authentication, RBAC (ADMIN / OPERATOR), Revocation & Audit
-- Reference: docs/decisions/DECISION_LOG.md (DEC-08)
-- Additive-only migration (safe to run against existing MySQL 8.4 database).
-- ==============================================================================

CREATE TABLE IF NOT EXISTS app_user (
    user_id VARCHAR(36) NOT NULL,
    username VARCHAR(50) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    role ENUM('ADMIN', 'OPERATOR') NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    provenance VARCHAR(20) NOT NULL DEFAULT 'SIMULATED',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id),
    CONSTRAINT uq_app_user_username UNIQUE (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_app_user_role ON app_user(role);

CREATE TABLE IF NOT EXISTS revoked_token (
    jti VARCHAR(36) NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    revoked_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expires_at DATETIME NOT NULL,
    PRIMARY KEY (jti),
    CONSTRAINT fk_revoked_token_user FOREIGN KEY (user_id) REFERENCES app_user(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_revoked_token_user ON revoked_token(user_id);
CREATE INDEX idx_revoked_token_expires ON revoked_token(expires_at);

CREATE TABLE IF NOT EXISTS auth_audit_log (
    audit_id VARCHAR(36) NOT NULL,
    username VARCHAR(50) NOT NULL,
    user_id VARCHAR(36) NULL,
    action ENUM('LOGIN_SUCCESS', 'LOGIN_FAILED', 'LOGOUT', 'ACCESS_DENIED', 'RATE_LIMITED') NOT NULL,
    role VARCHAR(20) NULL,
    endpoint VARCHAR(150) NULL,
    ip_address VARCHAR(64) NULL,
    detail VARCHAR(255) NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (audit_id),
    CONSTRAINT fk_auth_audit_user FOREIGN KEY (user_id) REFERENCES app_user(user_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_auth_audit_username ON auth_audit_log(username);
CREATE INDEX idx_auth_audit_action ON auth_audit_log(action);
CREATE INDEX idx_auth_audit_created_at ON auth_audit_log(created_at);
