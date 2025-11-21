

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, String, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class ErrorLog(BaseModel):
    """
    Persistent error log table for Nova.

    This table records significant errors emitted by different subsystems so that
    they can be inspected historically, even if in-memory logs roll over.

    Typical usages:
      - ingestion failures (Lunch Money, Apple Health, Whoop, etc.)
      - dashboard or automation crashes
      - unexpected API exceptions

    Fields:
      - source:         Short identifier of the subsystem that emitted the error
                        (e.g. "ingestion.lunchmoney", "dashboard.ui").
      - level:          Textual severity level (e.g. "ERROR", "WARNING", "CRITICAL").
      - message:        Short, human-readable summary of the error.
      - details:        Optional longer text (stack trace, JSON payload, etc.).
      - first_seen_at:  When this error instance was first recorded.
      - last_seen_at:   When this error instance was most recently seen.
      - occurrence_count: How many times this same error (or grouping key) occurred.
    """

    __tablename__ = "error_log"

    source: Mapped[str] = mapped_column(
        String(length=128),
        nullable=False,
        doc="Short identifier of the subsystem (e.g. 'ingestion.lunchmoney').",
    )

    level: Mapped[str] = mapped_column(
        String(length=32),
        nullable=False,
        default="ERROR",
        server_default="ERROR",
        doc="Severity level (e.g. ERROR, WARNING, CRITICAL).",
    )

    message: Mapped[str] = mapped_column(
        String(length=512),
        nullable=False,
        doc="Short, human-readable summary of the error.",
    )

    details: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Optional longer description, stack trace, or serialized payload.",
    )

    first_seen_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        doc="Timestamp when this error instance was first observed.",
    )

    last_seen_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        doc="Timestamp when this error instance was most recently observed.",
    )

    occurrence_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
        server_default="1",
        doc="Number of times this error (or grouping key) has occurred.",
    )