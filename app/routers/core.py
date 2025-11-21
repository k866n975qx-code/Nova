from datetime import datetime, timezone

from fastapi import APIRouter, Request

from app.config.settings import settings
from app.models.base import BaseResponse, Meta
from app.utils.logging_config import get_logger
from app.utils.meta import build_meta


router = APIRouter(tags=["core"])
logger = get_logger("nova.actions")


@router.get("/actions/handshake", response_model=BaseResponse)
async def actions_handshake(request: Request) -> BaseResponse:
    """Handshake endpoint for Nova Actions integration.

    Returns Nova/Doc version info and supported high-level domains so that
    external tools (like ChatGPT Actions) can understand what Nova can do.
    """

    # Optional Actions token guard:
    # - If settings.actions_api_token is None/empty -> handshake is open.
    # - If configured -> require matching token in the X-Nova-Actions-Token header.
    expected_token = getattr(settings, "actions_api_token", None)
    if expected_token:
        provided_token = request.headers.get("X-Nova-Actions-Token")
        if not provided_token or provided_token != expected_token:
            meta = build_meta()
            logger.warning(
                "Invalid or missing Actions token on handshake",
                extra={
                    "event_type": "actions_handshake_unauthorized",
                    "has_token": bool(provided_token),
                },
            )
            return BaseResponse(
                status="error",
                data={"error": "unauthorized", "reason": "invalid_actions_token"},
                meta=meta,
            )

    version = settings.version

    meta = build_meta()

    data = {
        "nova_version": version.get("version"),
        "master_doc_version": version.get("master_doc_version", "unknown"),
        "supported_domains": [
            "finance",
            "health",
            "training",
            "protocols",
            "automation",
            "system",
        ],
    }

    logger.info(
        "Actions handshake",
        extra={
            "event_type": "actions_handshake",
            "path": str(request.url.path),
        },
    )

    return BaseResponse(status="ok", data=data, meta=meta)