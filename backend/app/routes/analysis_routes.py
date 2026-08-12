from fastapi import APIRouter

from app.schemas.device_schema import AnalysisStatusResponse

router = APIRouter(tags=["Analysis"])


@router.get(
    "/status",
    response_model=AnalysisStatusResponse,
    summary="Analysis service status",
    description="Return the current analysis service status placeholder.",
)
async def analysis_status():
    return {"analysis": "not-implemented"}
