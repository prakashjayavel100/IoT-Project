from datetime import datetime
from typing import Dict, Optional

from pydantic import BaseModel, Field


class DeviceData(BaseModel):
    device_id: str = Field(..., description="Unique device identifier", json_schema_extra={"example": "device-123"})
    packet_rate: float = Field(..., json_schema_extra={"example": 12.5})
    behavior_score: float = Field(..., json_schema_extra={"example": 84.0})
    network_score: float = Field(..., json_schema_extra={"example": 73.2})
    firmware_score: float = Field(..., json_schema_extra={"example": 96.7})


class DeviceRecord(DeviceData):
    status: str = Field("TRUSTED", description="Computed device trust status")
    trust_score: float = Field(1.0, description="Computed device trust score")


class DeviceDataInput(BaseModel):
    packet_rate: float = Field(..., ge=0, description="Packet rate must be 0 or greater", json_schema_extra={"example": 12.5})
    behavior_score: float = Field(..., ge=0, le=100, description="Behavior score 0-100", json_schema_extra={"example": 84.0})
    network_score: float = Field(..., ge=0, le=100, description="Network score 0-100", json_schema_extra={"example": 73.2})
    firmware_score: float = Field(..., ge=0, le=100, description="Firmware score 0-100", json_schema_extra={"example": 96.7})


class DeviceRegister(BaseModel):
    device_id: str = Field(..., description="Unique device identifier", json_schema_extra={"example": "device-123"})
    device_name: str = Field(..., description="Human-friendly name", json_schema_extra={"example": "Factory Gateway"})
    device_type: str = Field(..., description="Type/category of device", json_schema_extra={"example": "gateway"})


class DeviceInDB(DeviceRegister):
    created_at: Optional[datetime] = Field(None, description="UTC timestamp when the device was registered")


class ActionResponse(BaseModel):
    success: bool = Field(..., json_schema_extra={"example": True})
    message: str = Field(..., json_schema_extra={"example": "Action completed successfully"})


class DeviceRegistrationResponse(ActionResponse):
    device: DeviceInDB


class DeviceDataReceivedResponse(BaseModel):
    device_id: str = Field(..., json_schema_extra={"example": "device-123"})
    packet_rate: float = Field(..., json_schema_extra={"example": 12.5})
    behavior_score: float = Field(..., json_schema_extra={"example": 84.0})
    network_score: float = Field(..., json_schema_extra={"example": 73.2})
    firmware_score: float = Field(..., json_schema_extra={"example": 96.7})
    timestamp: datetime = Field(..., json_schema_extra={"example": "2025-01-01T12:00:00Z"})
    message: str = Field(..., json_schema_extra={"example": "Device data received and stored"})


class AnalysisResultResponse(BaseModel):
    device_id: str = Field(..., json_schema_extra={"example": "device-123"})
    input_features: Dict[str, float] = Field(..., json_schema_extra={"example": {"packet_rate": 12.5, "behavior_score": 84.0, "network_score": 73.2, "firmware_score": 96.7}})
    anomaly_detected: bool = Field(..., json_schema_extra={"example": False})
    anomaly_score: float = Field(..., json_schema_extra={"example": 0.12})
    drift_detected: bool = Field(..., json_schema_extra={"example": False})
    trust_score: float = Field(..., json_schema_extra={"example": 0.94})
    status: str = Field(..., json_schema_extra={"example": "TRUSTED"})
    timestamp: datetime = Field(..., json_schema_extra={"example": "2025-01-01T12:00:00Z"})


class AnalysisHistoryItem(BaseModel):
    device_id: str = Field(..., json_schema_extra={"example": "device-123"})
    packet_rate: float = Field(..., json_schema_extra={"example": 12.5})
    behavior_score: float = Field(..., json_schema_extra={"example": 84.0})
    network_score: float = Field(..., json_schema_extra={"example": 73.2})
    firmware_score: float = Field(..., json_schema_extra={"example": 96.7})
    anomaly_detected: bool = Field(..., json_schema_extra={"example": False})
    anomaly_score: float = Field(..., json_schema_extra={"example": 0.12})
    drift_detected: bool = Field(..., json_schema_extra={"example": False})
    trust_score: float = Field(..., json_schema_extra={"example": 0.94})
    status: str = Field(..., json_schema_extra={"example": "TRUSTED"})
    timestamp: datetime = Field(..., json_schema_extra={"example": "2025-01-01T12:00:00Z"})


class NotificationResponse(BaseModel):
    device_id: str = Field(..., json_schema_extra={"example": "device-123"})
    status: str = Field(..., json_schema_extra={"example": "ANOMALY"})
    event_type: str = Field(..., json_schema_extra={"example": "ANOMALY"})
    description: str = Field(..., json_schema_extra={"example": "An anomaly was detected for this device."})
    trust_score: float = Field(..., json_schema_extra={"example": 0.35})
    level: str = Field(..., json_schema_extra={"example": "warning"})
    message: str = Field(..., json_schema_extra={"example": "An anomaly was detected in device behavior."})
    timestamp: datetime = Field(..., json_schema_extra={"example": "2025-01-01T12:00:00Z"})


class DashboardSummaryResponse(BaseModel):
    total_devices: int = Field(..., json_schema_extra={"example": 12})
    trusted_devices: int = Field(..., json_schema_extra={"example": 10})
    anomaly_devices: int = Field(..., json_schema_extra={"example": 1})
    drift_devices: int = Field(..., json_schema_extra={"example": 1})
    total_analysis_today: int = Field(..., json_schema_extra={"example": 4})
    critical_devices: int = Field(..., json_schema_extra={"example": 1})


class DashboardDeviceResponse(BaseModel):
    device_id: str = Field(..., json_schema_extra={"example": "device-123"})
    device_name: str = Field(..., json_schema_extra={"example": "Factory Gateway"})
    device_type: str = Field(..., json_schema_extra={"example": "gateway"})
    latest_trust_score: Optional[float] = Field(None, json_schema_extra={"example": 0.94})
    latest_status: Optional[str] = Field(None, json_schema_extra={"example": "TRUSTED"})
    latest_anomaly_result: Optional[bool] = Field(None, json_schema_extra={"example": False})
    latest_drift_result: Optional[bool] = Field(None, json_schema_extra={"example": False})
    latest_timestamp: Optional[datetime] = Field(None, json_schema_extra={"example": "2025-01-01T12:00:00Z"})


class HealthStatusResponse(BaseModel):
    status: str = Field(..., json_schema_extra={"example": "ok"})


class HealthDatabaseResponse(BaseModel):
    database: str = Field(..., json_schema_extra={"example": "ok"})


class RootResponse(BaseModel):
    message: str = Field(..., json_schema_extra={"example": "IoT Trust Drift Detection Backend"})


class AnalysisStatusResponse(BaseModel):
    analysis: str = Field(..., json_schema_extra={"example": "not-implemented"})