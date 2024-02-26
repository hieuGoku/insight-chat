"""Health router for the API."""

from fastapi import APIRouter

from app.api.database.models.health import HealthResponse

# Not authentication or authorization required to get the health status.
router = APIRouter()


@router.get("")
def health() -> HealthResponse:
    """Return ok if the system is up."""
    return HealthResponse(status="ok")
