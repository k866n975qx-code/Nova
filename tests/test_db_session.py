import os

import pytest

from app.db import session as db_session


def _reset_db_cache():
    """
    Helper to reset module-level engine/session caches between tests.
    """
    setattr(db_session, "_ENGINE", None)
    setattr(db_session, "_SESSION_LOCAL", None)


def test_get_database_url_raises_when_missing(monkeypatch):
    # Ensure no DB URL is configured
    monkeypatch.delenv("NOVA_DATABASE_URL", raising=False)
    monkeypatch.delenv("DATABASE_URL", raising=False)

    # If a future version of Settings ever adds database_url,
    # make sure it does not accidentally mask this test.
    if hasattr(db_session.settings, "database_url"):
        delattr(db_session.settings, "database_url")  # type: ignore[attr-defined]

    with pytest.raises(RuntimeError):
        db_session.get_database_url()


def test_get_database_url_prefers_nova_env(monkeypatch):
    nova_url = "postgresql+asyncpg://user:pass@localhost:5432/nova_test"
    fallback_url = "sqlite:///should_not_be_used.db"

    monkeypatch.setenv("NOVA_DATABASE_URL", nova_url)
    monkeypatch.setenv("DATABASE_URL", fallback_url)

    result = db_session.get_database_url()
    assert result == nova_url


def test_get_engine_uses_sqlite_memory_for_tests(monkeypatch):
    _reset_db_cache()

    # Use an in-memory SQLite URL so we don't require a real Postgres server
    monkeypatch.setenv("NOVA_DATABASE_URL", "sqlite:///:memory:")

    engine = db_session.get_engine(max_retries=1)
    assert engine is not None

    with engine.connect() as conn:
        result = conn.execute(db_session.text("SELECT 1")).scalar()
        assert result == 1


def test_get_session_yields_and_closes(monkeypatch):
    _reset_db_cache()

    monkeypatch.setenv("NOVA_DATABASE_URL", "sqlite:///:memory:")

    gen = db_session.get_session()
    db = next(gen)

    assert db is not None

    # Closing the generator should trigger db.close() in the finally block
    gen.close()