"""SQLAlchemy ORM model for Session."""

from datetime import datetime
from typing import List, Optional
from sqlalchemy import String, DateTime, Text, Enum as SQLEnum, CheckConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database.base import Base
from backend.app.models.enums import SessionStatus, DataProvenance


class Session(Base):
    __tablename__ = "session"

    session_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    end_time: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    environment: Mapped[str] = mapped_column(String(100), nullable=False)
    session_status: Mapped[SessionStatus] = mapped_column(
        SQLEnum(SessionStatus, native_enum=False),
        nullable=False,
        default=SessionStatus.INITIALIZING,
        index=True,
    )
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    provenance: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default=DataProvenance.SIMULATED.value,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Relationships
    tasks: Mapped[List["Task"]] = relationship(
        "Task",
        back_populates="session",
        cascade="all, delete-orphan",
    )
    decisions: Mapped[List["Decision"]] = relationship(
        "Decision",
        back_populates="session",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        CheckConstraint("end_time IS NULL OR end_time >= start_time", name="chk_session_times"),
    )
