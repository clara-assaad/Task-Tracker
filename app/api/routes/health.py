from datetime import datetime, timezone

from fastapi import APIRouter

from app.model_package.health import HealthResponse

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    """
    Simple health check endpoint.

    Returns HTTP 200 with a JSON body indicating service status
    and the current UTC timestamp in ISO 8601 format.
    """
    return HealthResponse(
        status="ok",
        timestamp=datetime.now(timezone.utc).isoformat(),
    )