from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app import database
from app.schemas.device_schema import HealthDatabaseResponse, HealthStatusResponse

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    response_model=HealthStatusResponse,
    summary="Health check",
    description="Return a simple liveness status for the API.",
)
async def health():
    return {"status": "ok"}


@router.get(
    "/health/database",
    response_model=HealthDatabaseResponse,
    summary="Database health check",
    description="Verify MongoDB connectivity for the application.",
    responses={503: {"description": "Database unreachable"}},
)
async def health_database():
    """Check MongoDB connectivity using a ping command."""
    try:
        ok = await database.ping_db()
    except Exception:
        ok = False

    if ok:
        return {"database": "ok"}
    return JSONResponse(status_code=503, content={"database": "unreachable"})
