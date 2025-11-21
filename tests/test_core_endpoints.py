import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.config.settings import settings

# ---------------------------------------------------------------------------
# Core endpoint and Actions API handshake tests
# ---------------------------------------------------------------------------


client = TestClient(app)


# ---------------------------------------------------------------------------
# Core status/version endpoint tests
# ---------------------------------------------------------------------------

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200

    body = response.json()
    # BaseResponse shape
    assert body["status"] == "ok"
    assert "data" in body
    assert "meta" in body

    meta = body["meta"]
    # Meta should at least carry a timestamp
    assert "timestamp" in meta
    # Version fields may be None/unknown, but keys should exist
    assert "nova_version" in meta
    assert "build" in meta


def test_status_endpoint():
    response = client.get("/status")
    assert response.status_code == 200

    body = response.json()
    # BaseResponse shape
    assert body["status"] == "ok"
    assert "data" in body
    assert "meta" in body

    data = body["data"]
    for key in ["system", "version", "build", "environment", "status", "uptime_seconds"]:
        assert key in data

    assert isinstance(data["uptime_seconds"], int)
    assert data["status"] == "online"


def test_version_endpoint():
    response = client.get("/version")
    assert response.status_code == 200

    body = response.json()
    # BaseResponse shape
    assert body["status"] == "ok"
    assert "data" in body
    assert "meta" in body

    data = body["data"]
    for key in ["nova_version", "build_date", "api_schema_version", "master_doc_version"]:
        assert key in data


# ---------------------------------------------------------------------------
# Actions API handshake tests
# ---------------------------------------------------------------------------
def test_actions_handshake_endpoint():
    response = client.get("/actions/handshake")
    assert response.status_code == 200

    body = response.json()
    # BaseResponse wrapper again
    assert body["status"] == "ok"
    assert "data" in body
    assert "meta" in body

    data = body["data"]
    assert "nova_version" in data
    assert "master_doc_version" in data

    supported = data.get("supported_domains", [])
    # Should be a non-empty list of domains
    assert isinstance(supported, list)
    assert len(supported) > 0
    assert "finance" in supported
    assert "health" in supported
    assert "training" in supported

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    body = response.json()
    # BaseResponse-style wrapper
    assert body["status"] == "ok"
    assert "data" in body
    assert "meta" in body

def test_actions_handshake_requires_token_when_configured():
    # Ensure a token is configured
    original_token = settings.actions_api_token
    settings.actions_api_token = "test-secret-token"
    try:
        response = client.get("/actions/handshake")
        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "error"
        data = body.get("data", {})
        assert data.get("error") == "unauthorized"
        assert data.get("reason") == "invalid_actions_token"
    finally:
        # Restore original token to avoid test leakage
        settings.actions_api_token = original_token


def test_actions_handshake_accepts_valid_token():
    # Ensure a token is configured
    original_token = settings.actions_api_token
    settings.actions_api_token = "test-secret-token"
    try:
        response = client.get(
            "/actions/handshake",
            headers={"X-Nova-Actions-Token": "test-secret-token"},
        )
        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "ok"
        data = body.get("data", {})
        # sanity check that handshake still returns expected fields
        assert "nova_version" in data
        assert "master_doc_version" in data
        assert "supported_domains" in data
    finally:
        # Restore original token to avoid test leakage
        settings.actions_api_token = original_token