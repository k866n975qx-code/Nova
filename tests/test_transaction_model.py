from __future__ import annotations

import sqlalchemy
from sqlalchemy.engine import Engine

from app.db import session as db_session
from app.db.models.base import Base
from app.db.models.transaction import Transaction  # noqa: F401  (import ensures model is registered)


def _reset_db_cache() -> None:
    """
    Helper to reset module-level engine/session caches between tests.
    """
    setattr(db_session, "_ENGINE", None)
    setattr(db_session, "_SESSION_LOCAL", None)


def _make_engine_sqlite_memory(monkeypatch) -> Engine:
    """
    Create a fresh in-memory SQLite engine using Nova's DB session helper.
    """
    _reset_db_cache()
    monkeypatch.setenv("NOVA_DATABASE_URL", "sqlite:///:memory:")
    return db_session.get_engine(max_retries=1)


def test_transactions_table_can_be_created(monkeypatch):
    """
    Basic integration test to ensure the Transaction model is wired correctly and
    its table can be created against the current Base metadata.
    """
    engine = _make_engine_sqlite_memory(monkeypatch)

    # This will raise if the model/metadata is misconfigured.
    Base.metadata.create_all(bind=engine)

    inspector = sqlalchemy.inspect(engine)
    tables = inspector.get_table_names()
    assert "transactions" in tables


def test_transactions_table_has_expected_columns(monkeypatch):
    """
    Ensure the transactions table exposes the expected column names, including
    those inherited from BaseModel (id, created_at, updated_at).
    """
    engine = _make_engine_sqlite_memory(monkeypatch)

    Base.metadata.create_all(bind=engine)
    inspector = sqlalchemy.inspect(engine)

    column_names = {col["name"] for col in inspector.get_columns("transactions")}

    expected = {
        "id",
        "created_at",
        "updated_at",
        "source",
        "external_id",
        "account_external_id",
        "txn_date",
        "amount",
        "currency",
        "payee",
        "category",
        "notes",
        "is_pending",
        "is_transfer",
        "cleared_at",
    }
    assert expected.issubset(column_names)
