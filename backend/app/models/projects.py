from uuid import uuid4, UUID
from datetime import datetime
from sqlalchemy import String,func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import UniqueConstraint
from app.helpers.db import Base


class ProjectsDB(Base):
    """
    Projects table Schema
    """
    __tablename__ = "projects"

    project_id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4
    )

    project_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True
    )

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False
    )