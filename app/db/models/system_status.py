

from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class SystemStatus(BaseModel):
    """
    High-level runtime and health state for Nova components.

    Intended to have a small number of rows (for example, one per major component),
    such as:
      - "nova-core"
      - "ingestion"
      - "dashboard"
      - "automation"

    Fields:
      - name:               Logical name of the component or subsystem.
      - is_healthy:         Current overall health flag for this component.
      - last_heartbeat:     Last time this component reported a heartbeat.
      - last_error_at:      Timestamp of the most recent error, if any.
      - last_error_message: Message or summary of the most recent error.
      - error_count:        Cumulative number of errors observed.
    """

    __tablename__ = "system_status"

    name: Mapped[str] = mapped_column(
        String(length=64),
        nullable=False,
        doc="Name of the component or subsystem (e.g. 'nova-core', 'ingestion').",
    )

    is_healthy: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="1",
        doc="True if the component is considered healthy.",
    )

    last_heartbeat: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        doc="Last time this component reported a heartbeat.",
    )

    last_error_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        doc="Timestamp of the most recent error, if any.",
    )

    last_error_message: Mapped[str | None] = mapped_column(
        String(length=512),
        nullable=True,
        doc="Message or summary of the most recent error.",
    )

    error_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
        doc="Cumulative count of errors observed for this component.",
    )