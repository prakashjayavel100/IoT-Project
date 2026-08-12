from datetime import datetime
from typing import List

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from app.schemas.device_schema import (
    ActionResponse,
    AnalysisResultResponse,
    DeviceDataInput,
    DeviceInDB,
    DeviceRegister,
    DeviceDataReceivedResponse,
    DeviceRegistrationResponse,
)
from app import database
from app.services.analysis_service import analyze_device

# Router prefix matches the requested API path: /api/devices
router = APIRouter(prefix="/api/devices", tags=["Devices"])


@router.post(
    "",
    response_model=DeviceRegistrationResponse,
    summary="Register a new device",
    description="Register a device with a unique device_id to begin IoT trust and drift monitoring.",
    responses={409: {"description": "Device with this device_id already exists"}},
)
async def register_device(payload: DeviceRegister):
    # Check duplicate
    existing = await database.get_device(payload.device_id)
    if existing:
        return JSONResponse(status_code=409, content={
            "success": False,
            "message": "Device with this device_id already exists",
            "device_id": payload.device_id,
        })

    device_doc = {
        "device_id": payload.device_id,
        "device_name": payload.device_name,
        "device_type": payload.device_type,
    }
    await database.insert_device(device_doc)
    saved = await database.get_device(payload.device_id)
    return {"success": True, "message": "Device registered successfully", "device": saved}


@router.post(
    "/{device_id}/data",
    response_model=DeviceDataReceivedResponse,
    summary="Submit raw device telemetry",
    description="Store raw telemetry data for later analysis and monitoring.",
    responses={404: {"description": "Device not found"}, 500: {"description": "Database error"}},
)
async def post_device_data(device_id: str, payload: DeviceDataInput):
    device = await database.get_device(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    try:
        await database.insert_raw_device_data(device_id, payload.dict())
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Database error: {exc}")

    return {
        "device_id": device_id,
        "packet_rate": payload.packet_rate,
        "behavior_score": payload.behavior_score,
        "network_score": payload.network_score,
        "firmware_score": payload.firmware_score,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "message": "Device data received and stored",
    }


@router.post(
    "/{device_id}/analyze",
    response_model=AnalysisResultResponse,
    summary="Analyze a device data sample",
    description="Run anomaly detection, drift monitoring, and trust scoring for a device input payload.",
    responses={404: {"description": "Device not found or analysis failed"}},
)
async def analyze_device_route(device_id: str, payload: DeviceDataInput):
    # Step 1: Verify the device exists.
    device = await database.get_device(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    # Step 2: Validate incoming data is handled by Pydantic via DeviceDataInput.
    input_data = payload.dict()

    try:
        result = await analyze_device(device_id, input_data)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {exc}")

    return result


@router.get(
    "",
    response_model=List[DeviceInDB],
    summary="List all registered devices",
    description="Return recent registered devices and their registration metadata.",
)
async def list_devices():
    devices = await database.get_all_devices()
    return devices


@router.get(
    "/{device_id}",
    response_model=DeviceInDB,
    summary="Get device details",
    description="Fetch a registered device by its device_id.",
    responses={404: {"description": "Device not found"}},
)
async def get_device(device_id: str):
    device = await database.get_device(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device


@router.delete(
    "/{device_id}",
    response_model=ActionResponse,
    summary="Delete a registered device",
    description="Delete a device record by device_id.",
    responses={404: {"description": "Device not found"}},
)
async def delete_device(device_id: str):
    deleted = await database.delete_device(device_id)
    if deleted:
        return {"success": True, "message": "Device deleted"}
    raise HTTPException(status_code=404, detail="Device not found")
