"""SQLAlchemy ORM model for SystemEvent."""

from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime, Text, Enum as SQLEnum, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database.base import Base
from backend.app.models.enums import EventType, ResolutionStatus, DataProvenance


class SystemEvent(Base):
    __tablename__ = "system_event"

    event_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    device_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("device.device_id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    operation_id: Mapped[Optional[str]] = mapped_column(
        String(36),
        ForeignKey("operation.operation_id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    event_time: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    event_type: Mapped[EventType] = mapped_column(
        SQLEnum(EventType, native_enum=False),
        nullable=False,
        default=EventType.INFO,
        index=True,
    )
    description: Mapped[str] = mapped_column(Text, nullable=False)
    resolution_status: Mapped[ResolutionStatus] = mapped_column(
        SQLEnum(ResolutionStatus, native_enum=False),
        nullable=False,
        default=ResolutionStatus.OPEN,
        index=True,
    )
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
    device: Mapped["Device"] = relationship("Device", back_populates="system_events")
    operation: Mapped[Optional["Operation"]] = relationship("Operation", back_populates="system_events")
