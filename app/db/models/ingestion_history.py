from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class IngestionHistory(BaseModel):
    """
    History of ingestion runs for external data sources (Lunch Money, Apple Health,
    Whoop, Intervals, etc.).

    Each row represents a single ingestion attempt or run for a given source.

    Fields:
      - source:            Identifier for the data source or pipeline
                           (e.g. "lunchmoney", "apple_health", "whoop").
      - status:            High-level result of the run
                           (e.g. "SUCCESS", "FAILED", "PARTIAL", "RUNNING").
      - started_at:        When this ingestion run started.
      - finished_at:       When this ingestion run finished (if known).
      - records_total:     Total number of records discovered/considered.
      - records_success:   Number of records successfully processed.
      - records_failed:    Number of records that failed or were skipped.
      - run_id:            Optional external identifier or correlation ID.
    """

    __tablename__ = "ingestion_history"

    source: Mapped[str] = mapped_column(
        String(length=64),
        nullable=False,
        doc="Identifier for the data source (e.g. 'lunchmoney', 'apple_health').",
    )

    status: Mapped[str] = mapped_column(
        String(length=32),
        nullable=False,
        default="RUNNING",
        server_default="RUNNING",
        doc="High-level status of the run (e.g. SUCCESS, FAILED, PARTIAL, RUNNING).",
    )

    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        doc="Timestamp when this ingestion run started.",
    )

    finished_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        doc="Timestamp when this ingestion run finished.",
    )

    records_total: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
        doc="Total number of records discovered/considered in this run.",
    )

    records_success: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
        doc="Number of records successfully processed.",
    )

    records_failed: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
        doc="Number of records that failed or were skipped.",
    )

    run_id: Mapped[str | None] = mapped_column(
        String(length=128),
        nullable=True,
        doc="Optional external run identifier or correlation ID.",
    )
