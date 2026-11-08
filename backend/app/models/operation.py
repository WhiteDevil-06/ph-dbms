"""SQLAlchemy ORM model for Operation."""

from datetime import datetime
from typing import List, Optional
from sqlalchemy import String, DateTime, Text, Enum as SQLEnum, ForeignKey, CheckConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database.base import Base
from backend.app.models.enums import OperationStatus, DataProvenance


class Operation(Base):
    __tablename__ = "operation"

    operation_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    task_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("task.task_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    device_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("device.device_id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    operation_type: Mapped[str] = mapped_column(String(50), nullable=False)
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_time: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    operation_status: Mapped[OperationStatus] = mapped_column(
        SQLEnum(OperationStatus, native_enum=False),
        nullable=False,
        default=OperationStatus.IN_PROGRESS,
        index=True,
    )
    result: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
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
    task: Mapped["Task"] = relationship("Task", back_populates="operations")
    device: Mapped["Device"] = relationship("Device", back_populates="operations")
    system_events: Mapped[List["SystemEvent"]] = relationship(
        "SystemEvent",
        back_populates="operation",
    )

    __table_args__ = (
        CheckConstraint("end_time IS NULL OR end_time >= start_time", name="chk_op_times"),
    )
