from datetime import datetime, timezone

from fastapi import APIRouter

from app.model_package.health import HealthResponse

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    """Performs a simple health check.

    Returns:
        HealthResponse: A HealthResponse object indicating service status ("ok")
        and the current UTC timestamp in ISO 8601 format.

    Examples:
        >>> # Request to health check
        >>> client.get("/health")
        200 OK
    """
    return HealthResponse(
        status="ok",
        timestamp=datetime.now(timezone.utc).isoformat(),
    )