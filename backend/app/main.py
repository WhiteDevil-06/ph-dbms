"""FastAPI Application Entrypoint — Post-Harvest DBMS Layer.

Intelligent Data Management and Operational Analytics for Autonomous Post-Harvest Material Handling Systems.
NOTE: This is a foundation starter scaffold. Application services and database repositories
are implemented following the Architecture Gate review.
"""

import os
from datetime import datetime, timezone
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI application
app = FastAPI(
    title="Post-Harvest Material Handling DBMS API",
    description="Operational persistence, detection indexing, and analytics layer for autonomous post-harvest robotics.",
    version="0.1.0-scaffold",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Configuration
allowed_origins = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:5173,http://127.0.0.1:5173"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in allowed_origins if origin.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["System"])
def health_check():
    """Health check endpoint.

    Reports system runtime state and active data source mode.
    NOTE: Database connectivity checks will be wired to active sessions after database setup.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": "0.1.0-scaffold",
        "data_source_mode": os.getenv("DATA_SOURCE_MODE", "SIMULATION"),
        "services": {
            "mysql": "NOT_CONNECTED_SCAFFOLD",
            "mongodb": "NOT_CONNECTED_SCAFFOLD",
        },
        "provenance_policy": "SIMULATION_ONLY",
    }


@app.get("/api/v1/simulation/status", tags=["Simulation"])
def simulation_status():
    """Returns the current simulation engine configuration and active seed."""
    return {
        "mode": "SIMULATED",
        "active_seed": int(os.getenv("SIMULATION_DEFAULT_SEED", "42")),
        "status": "SCAFFOLD_READY",
        "counts": {
            "sessions": 0,
            "tasks": 0,
            "operations": 0,
            "detections": 0,
            "decisions": 0,
            "system_events": 0,
        },
        "notes": "Full generator logic and database insertion will be activated after Architecture Gate approval.",
    }

