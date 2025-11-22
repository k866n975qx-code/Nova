

from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class Transaction(BaseModel):
    """
    Phase 2.4 – Finance Tables: Transaction

    Represents a single financial transaction imported from an external system
    (e.g. Lunch Money) or created locally in Nova.

    This is intentionally generic so it can support:
      - bank/credit card transactions
      - cash/manual entries
      - investment-related cash movements (at a basic level)

    Fields:
      - source:              Origin system (e.g. "lunchmoney", "manual").
      - external_id:         Optional transaction ID from the source system.
      - account_external_id: Optional external ID of the related account in the
                             source system (to be linked to Account.external_id
                             at the ingestion/service layer).
      - txn_date:            Posting/transaction date (no time-of-day).
      - amount:              Signed amount (credits vs debits) in account currency.
      - currency:            ISO currency code (e.g. "USD").
      - payee:               Optional payee/merchant name.
      - category:            Optional category label (source or normalized).
      - notes:               Optional free-form notes/memo.
      - is_pending:          True if the transaction is pending/uncleared.
      - is_transfer:         True if the transaction is part of an internal transfer.
      - cleared_at:          Timestamp when the transaction was confirmed/cleared.
    """

    __tablename__ = "transactions"

    source: Mapped[str] = mapped_column(
        String(length=32),
        nullable=False,
        default="lunchmoney",
        server_default="lunchmoney",
        doc="Source system for this transaction (e.g. 'lunchmoney', 'manual').",
    )

    external_id: Mapped[str | None] = mapped_column(
        String(length=128),
        nullable=True,
        doc="External transaction identifier from the source system, if any.",
    )

    account_external_id: Mapped[str | None] = mapped_column(
        String(length=128),
        nullable=True,
        doc=(
            "External account identifier from the source system. Intended to be"
            " linked to Account.external_id in ingestion/service logic."
        ),
    )

    txn_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
        doc="Transaction/posting date (no time-of-day).",
    )

    amount: Mapped[float] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        doc="Signed transaction amount in the account's currency.",
    )

    currency: Mapped[str] = mapped_column(
        String(length=8),
        nullable=False,
        default="USD",
        server_default="USD",
        doc="ISO currency code (e.g. 'USD').",
    )

    payee: Mapped[str | None] = mapped_column(
        String(length=256),
        nullable=True,
        doc="Optional payee or merchant name.",
    )

    category: Mapped[str | None] = mapped_column(
        String(length=128),
        nullable=True,
        doc="Optional category label (source-provided or normalized).",
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Optional free-form notes or memo associated with the transaction.",
    )

    is_pending: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default="0",
        doc="True if this transaction is pending/uncleared.",
    )

    is_transfer: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default="0",
        doc="True if this transaction is part of an internal transfer.",
    )

    cleared_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        doc="Timestamp when this transaction was confirmed/cleared.",
    )