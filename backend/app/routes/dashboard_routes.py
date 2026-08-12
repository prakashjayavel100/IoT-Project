from typing import List

from fastapi import APIRouter, HTTPException

from app import database
from app.schemas.device_schema import (
    AnalysisHistoryItem,
    DashboardDeviceResponse,
    DashboardSummaryResponse,
)

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get(
    "/summary",
    response_model=DashboardSummaryResponse,
    summary="Dashboard summary",
    description="Return aggregated counts for the dashboard overview.",
)
async def dashboard_summary():
    return await database.get_dashboard_summary()


@router.get(
    "/devices",
    response_model=List[DashboardDeviceResponse],
    summary="Dashboard device list",
    description="Return devices and their latest trust analysis metadata.",
)
async def dashboard_devices():
    return await database.get_dashboard_devices()


@router.get(
    "/devices/{device_id}/history",
    response_model=List[AnalysisHistoryItem],
    summary="Device analysis history",
    description="Return analysis history entries for a specific device.",
    responses={404: {"description": "No history found for this device"}},
)
async def device_history(device_id: str):
    history = await database.get_analysis_history(device_id)
    if not history:
        raise HTTPException(status_code=404, detail="No history found for this device")
    return history
