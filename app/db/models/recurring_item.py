

from __future__ import annotations

from datetime import date

from sqlalchemy import Boolean, Date, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class RecurringItem(BaseModel):
    """
    Phase 2.4 – Finance Tables: RecurringItem

    Represents a recurring financial item such as a subscription, recurring bill,
    or scheduled transfer. This is intentionally generic so it can model:

      - rent, utilities, insurance
      - phone/internet subscriptions
      - streaming services
      - recurring savings transfers

    Fields:
      - source:          Origin system (e.g. "lunchmoney", "manual").
      - external_id:     Optional recurring item ID from the source system.
      - name:            Human-friendly label (e.g. "Rent", "Phone Bill").
      - payee:           Optional payee/merchant name.
      - category:        Optional category or tag.
      - amount:          Expected amount per occurrence.
      - currency:        ISO currency code (e.g. "USD").
      - frequency:       Recurrence pattern as a string
                         (e.g. "monthly", "weekly", "biweekly", "yearly").
      - next_occurrence: Next due/expected date for this recurring item.
      - last_occurrence: Last date this item occurred (if known).
      - is_active:       True if this recurring item is currently in effect.
      - notes:           Optional free-form notes.
    """

    __tablename__ = "recurring_items"

    source: Mapped[str] = mapped_column(
        String(length=32),
        nullable=False,
        default="lunchmoney",
        server_default="lunchmoney",
        doc="Source system for this recurring item (e.g. 'lunchmoney', 'manual').",
    )

    external_id: Mapped[str | None] = mapped_column(
        String(length=128),
        nullable=True,
        doc="External recurring item identifier from the source system, if any.",
    )

    name: Mapped[str] = mapped_column(
        String(length=128),
        nullable=False,
        doc="Human-friendly name for this recurring item (e.g. 'Rent').",
    )

    payee: Mapped[str | None] = mapped_column(
        String(length=256),
        nullable=True,
        doc="Optional payee or merchant name.",
    )

    category: Mapped[str | None] = mapped_column(
        String(length=128),
        nullable=True,
        doc="Optional category or tag for this recurring item.",
    )

    amount: Mapped[float] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        doc="Expected amount per occurrence in the specified currency.",
    )

    currency: Mapped[str] = mapped_column(
        String(length=8),
        nullable=False,
        default="USD",
        server_default="USD",
        doc="ISO currency code (e.g. 'USD').",
    )

    frequency: Mapped[str | None] = mapped_column(
        String(length=32),
        nullable=True,
        doc="Recurrence pattern (e.g. 'monthly', 'weekly', 'biweekly', 'yearly').",
    )

    next_occurrence: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
        doc="Next expected date for this recurring item.",
    )

    last_occurrence: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
        doc="Most recent date this recurring item occurred.",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="1",
        doc="True if this recurring item is currently active.",
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Optional free-form notes about this recurring item.",
    )