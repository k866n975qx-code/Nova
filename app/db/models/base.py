

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """
    Root SQLAlchemy declarative base for all Nova models.

    All persistent tables should ultimately inherit from BaseModel
    (which itself inherits from this Base).
    """
    pass


class TimestampMixin:
    """
    Mixin that provides created_at / updated_at timestamp columns.

    - created_at: when the row was first inserted
    - updated_at: automatically updated on each change
    """
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class UUIDPrimaryKeyMixin:
    """
    Mixin that provides a UUID primary key column named `id`.
    """
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )


class BaseModel(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """
    Abstract base class for all Nova tables.

    Inherit from this in concrete models, e.g.:

        class Meta(BaseModel):
            __tablename__ = "meta"
            # additional columns...

    This ensures every table has:
      - id (UUID primary key)
      - created_at / updated_at timestamps
    """
    __abstract__ = True

    def __repr__(self) -> str:
        info = []
        if hasattr(self, "id"):
            info.append(f"id={self.id!r}")
        return f"<{self.__class__.__name__} {' '.join(info)}>"