"""Application configuration management using Pydantic Settings."""

from typing import List, Union
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # Application
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    # Server
    BACKEND_HOST: str = "127.0.0.1"
    BACKEND_PORT: int = 8000
    API_V1_PREFIX: str = "/api/v1"
    CORS_ORIGINS: Union[List[str], str] = ["http://localhost:5173", "http://127.0.0.1:5173"]

    # Provenance and Simulation
    DATA_SOURCE_MODE: str = "SIMULATION"
    SIMULATION_DEFAULT_SEED: int = 42
    ENABLE_SIMULATION_RESET: bool = True

    # MySQL Database
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = 3306
    MYSQL_DATABASE: str = "post_harvest_db"
    MYSQL_USER: str = "post_harvest_app"
    MYSQL_PASSWORD: str = "apppassword_local"
    MYSQL_ROOT_PASSWORD: str = "rootpassword_local"
    DATABASE_URL: str = (
        "mysql+pymysql://post_harvest_app:apppassword_local@localhost:3306/post_harvest_db"
    )

    # MongoDB Telemetry Database
    MONGODB_HOST: str = "localhost"
    MONGODB_PORT: int = 27017
    MONGODB_DATABASE: str = "post_harvest_telemetry"
    MONGODB_USER: str = "admin"
    MONGODB_PASSWORD: str = "adminpassword_local"
    MONGODB_URI: str = (
        "mongodb://admin:adminpassword_local@localhost:27017/post_harvest_telemetry?authSource=admin"
    )

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str):
            if v.startswith("[") and v.endswith("]"):
                import json
                try:
                    return json.loads(v)
                except Exception:
                    pass
            return [i.strip() for i in v.split(",") if i.strip()]
        return v


settings = Settings()
