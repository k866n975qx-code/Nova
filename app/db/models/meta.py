from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class Meta(BaseModel):
    """
    Core metadata table for the Nova database.

    This table is intended to have a very small number of rows (often just one)
    and tracks high-level information about the schema and build.

    Fields:
      - db_version:      Semantic version or internal schema version string.
      - last_migration:  Identifier/name of the last applied migration.
      - build_date:      When this database instance/schema was created.
    """

    __tablename__ = "meta"

    db_version: Mapped[str] = mapped_column(
        String(length=64),
        nullable=False,
        doc="Semantic or internal version string for the DB/schema.",
    )

    last_migration: Mapped[str | None] = mapped_column(
        String(length=128),
        nullable=True,
        doc="Identifier or name of the last applied migration.",
    )

    build_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        doc="Timestamp of when this DB/schema was first created.",
    )
