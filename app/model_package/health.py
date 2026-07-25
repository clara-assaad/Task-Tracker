from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Response shape for the /health endpoint."""
    status: str
    timestamp: str