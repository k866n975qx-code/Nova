import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException

from app.main import app

# ---------------------------------------------------------------------------
# Error handler and 4xx/5xx response structure tests
# ---------------------------------------------------------------------------


# Attach a test-only route that will raise an unhandled exception
@app.get("/test-internal-error")
async def internal_error_route():  # pragma: no cover - logic tested via handler
    raise RuntimeError("boom")

@app.get("/test-http-error")
async def http_error_route():  # pragma: no cover - logic tested via handler
    raise HTTPException(status_code=404, detail="Not Found")


client = TestClient(app, raise_server_exceptions=False)


# ---------------------------------------------------------------------------
# Error handler structure tests (HTTP 404 / 500)
# ---------------------------------------------------------------------------

def test_http_404_error_structure():
    response = client.get("/test-http-error")
    assert response.status_code == 404

    body = response.json()
    assert "error" in body
    assert "meta" in body

    error = body["error"]
    assert error["code"] == "http_404"
    assert isinstance(error["message"], str)

    meta = body["meta"]
    assert "timestamp" in meta
    assert "nova_version" in meta
    assert "build" in meta


def test_internal_error_handler_structure():
    response = client.get("/test-internal-error")
    assert response.status_code == 500

    body = response.json()
    assert "error" in body
    assert "meta" in body

    error = body["error"]
    assert error["code"] == "internal_error"
    assert isinstance(error["message"], str)

    meta = body["meta"]
    assert "timestamp" in meta
    assert "nova_version" in meta
    assert "build" in meta


# ---------------------------------------------------------------------------
# Unknown route behavior tests
# ---------------------------------------------------------------------------
def test_unknown_path_returns_404():
    response = client.get("/this-path-does-not-exist")
    assert response.status_code == 404
