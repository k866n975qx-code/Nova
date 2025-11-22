

from __future__ import annotations

from datetime import date

from sqlalchemy import Boolean, Date, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class Budget(BaseModel):
    """
    Phase 2.4 – Finance Tables: Budget

    Represents a budget for a given period, optionally tied to a category or
    grouping. This is designed to support:
      - category-level budgets (e.g. "Groceries", "Dining Out")
      - global/monthly budgets
      - imported external budgets from systems like Lunch Money

    Fields:
      - source:        Origin system (e.g. "lunchmoney", "manual").
      - external_id:   Optional external budget ID from the source system.
      - name:          Human-friendly name for this budget.
      - category:      Optional category/tag this budget applies to.
      - period_start:  Start date (inclusive) of the budget period.
      - period_end:    End date (inclusive) of the budget period.
      - limit_amount:  Maximum allowed spending for this budget period.
      - currency:      ISO currency code (e.g. "USD").
      - is_active:     True if this budget is currently in effect.
    """

    __tablename__ = "budgets"

    source: Mapped[str] = mapped_column(
        String(length=32),
        nullable=False,
        default="lunchmoney",
        server_default="lunchmoney",
        doc="Source system for this budget (e.g. 'lunchmoney', 'manual').",
    )

    external_id: Mapped[str | None] = mapped_column(
        String(length=128),
        nullable=True,
        doc="External budget identifier from the source system, if any.",
    )

    name: Mapped[str] = mapped_column(
        String(length=128),
        nullable=False,
        doc="Human-friendly name for this budget.",
    )

    category: Mapped[str | None] = mapped_column(
        String(length=128),
        nullable=True,
        doc="Optional category or tag this budget applies to.",
    )

    period_start: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
        doc="Start date (inclusive) of the budget period.",
    )

    period_end: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
        doc="End date (inclusive) of the budget period.",
    )

    limit_amount: Mapped[float] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        doc="Maximum allowed spending for this budget period.",
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
        doc="True if this budget is currently active.",
    )