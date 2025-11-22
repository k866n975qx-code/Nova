

from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class Account(BaseModel):
    """
    Phase 2.4 – Finance Tables: Account

    Represents a financial account imported from an external source (e.g. Lunch
    Money) or defined locally in Nova.

    This table is intentionally generic so it can represent:
      - checking/savings accounts
      - credit cards and lines of credit
      - investment/brokerage accounts
      - cash or manual accounts

    Fields:
      - source:          Short identifier for where this account came from
                         (e.g. "lunchmoney", "manual", "mock").
      - external_id:     Optional external ID from the source system.
      - name:            Human-readable account name.
      - type:            High-level type (e.g. "cash", "credit", "investment").
      - subtype:         Provider-specific subtype or further classification.
      - currency:        ISO currency code (e.g. "USD").
      - is_active:       False if the account has been closed/archived.
      - is_excluded:     True if this account is excluded from net worth or
                         aggregate calculations.
      - institution_name: Optional display name of institution/provider.
      - last_synced_at:  Timestamp of the last successful sync for this account.
    """

    __tablename__ = "accounts"

    source: Mapped[str] = mapped_column(
        String(length=32),
        nullable=False,
        default="lunchmoney",
        server_default="lunchmoney",
        doc="Source system for this account (e.g. 'lunchmoney', 'manual').",
    )

    external_id: Mapped[str | None] = mapped_column(
        String(length=128),
        nullable=True,
        doc="External identifier from the source system, if any.",
    )

    name: Mapped[str] = mapped_column(
        String(length=128),
        nullable=False,
        doc="Human-readable name of the account.",
    )

    type: Mapped[str | None] = mapped_column(
        String(length=64),
        nullable=True,
        doc="High-level account type (e.g. 'cash', 'credit', 'investment').",
    )

    subtype: Mapped[str | None] = mapped_column(
        String(length=64),
        nullable=True,
        doc="Provider-specific subtype or further classification.",
    )

    currency: Mapped[str] = mapped_column(
        String(length=8),
        nullable=False,
        default="USD",
        server_default="USD",
        doc="ISO currency code (e.g. 'USD').",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="1",
        doc="False if the account has been closed/archived.",
    )

    is_excluded: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default="0",
        doc="True if this account is excluded from aggregate calculations.",
    )

    institution_name: Mapped[str | None] = mapped_column(
        String(length=128),
        nullable=True,
        doc="Optional display name of the institution/provider.",
    )

    last_synced_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        doc="Timestamp of the last successful sync for this account.",
    )