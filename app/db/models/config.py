

from __future__ import annotations

from sqlalchemy import Boolean, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class Config(BaseModel):
    """
    Dynamic configuration table for Nova.

    This table stores key/value style settings that can be changed without
    redeploying code. It is intended for things like:

      - feature flags
      - ingestion tuning parameters
      - thresholds (e.g. alert levels, retry limits)
      - integration toggles (enable/disable certain subsystems)

    Fields:
      - key:         Unique identifier for the setting.
      - value:       Text representation of the value (raw string or JSON).
      - group:       Optional grouping/category name (e.g. "finance", "health", "system").
      - description: Optional human-readable explanation of what this setting controls.
      - is_active:   Whether this setting is currently in effect.
    """

    __tablename__ = "config"

    key: Mapped[str] = mapped_column(
        String(length=128),
        nullable=False,
        unique=True,
        doc="Unique identifier for the setting.",
    )

    value: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        doc="Text or JSON-encoded representation of the setting value.",
    )

    group: Mapped[str | None] = mapped_column(
        String(length=64),
        nullable=True,
        doc="Optional grouping/category (e.g. 'finance', 'health', 'system').",
    )

    description: Mapped[str | None] = mapped_column(
        String(length=512),
        nullable=True,
        doc="Optional human-readable explanation of this setting.",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="1",
        doc="True if this setting is currently active.",
    )