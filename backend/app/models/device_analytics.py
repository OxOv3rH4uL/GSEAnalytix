from uuid import uuid4, UUID
from datetime import datetime
from sqlalchemy import func, Float, ForeignKey, Numeric
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import CheckConstraint
from decimal import Decimal
from app.helpers.db import Base

class Analytics(Base):
    """
    Energy Analysis Table Schema
    """
    __tablename__ = "energy_analysis"
    __table_args__ = (
        CheckConstraint("total_runtime > 0"),
        CheckConstraint("total_cost > 0"),
        CheckConstraint("total_kwh > 0")
    )

    
    device_id: Mapped[UUID] = mapped_column(
        ForeignKey("devices.device_id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False
    )
    total_runtime: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )
    total_kwh: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )
    total_cost: Mapped[Decimal] = mapped_column(
        Numeric(10,2),
        nullable=False,
        default=Decimal("0")
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False
    )
    