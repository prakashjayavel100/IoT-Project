import logging
from datetime import datetime, timezone
from typing import Dict

from app.schemas.device_schema import DeviceDataInput
from app import database
from app.services import feature_service, anomaly_service, drift_service, trust_service
from app.services.notification_service import create_notification


async def analyze_device(device_id: str, input_data: Dict[str, float]) -> Dict[str, object]:
    """Run the full analysis pipeline for a single device.

    This service keeps the routing layer separate from the ML and database logic.
    """
    device = await database.get_device(device_id)
    if not device:
        raise ValueError("Device not found")

    validated = DeviceDataInput(**input_data)
    validated_data = validated.model_dump()
    features = feature_service.extract_features(validated_data)

    model = anomaly_service.get_default_isolation_forest()
    anomaly_result = anomaly_service.detect_anomaly(features, model)

    drift_result = drift_service.detect_drift(device_id, validated_data)

    trust_result = trust_service.compute_trust_score({
        "behavior_score": validated.behavior_score,
        "network_score": validated.network_score,
        "firmware_score": validated.firmware_score,
        "anomaly_detected": anomaly_result["anomaly_detected"],
        "anomaly_score": anomaly_result["anomaly_score"],
        "drift_detected": drift_result["drift_detected"],
    })

    now = datetime.now(timezone.utc)
    result = {
        "device_id": device_id,
        "input_features": validated_data,
        "anomaly_detected": anomaly_result["anomaly_detected"],
        "anomaly_score": anomaly_result["anomaly_score"],
        "drift_detected": drift_result["drift_detected"],
        "trust_score": trust_result["trust_score"],
        "status": trust_result["status"],
        "timestamp": now.isoformat().replace('+00:00', 'Z'),
    }

    try:
        await database.store_analysis({
            "device_id": device_id,
            **validated_data,
            "anomaly_detected": anomaly_result["anomaly_detected"],
            "anomaly_score": anomaly_result["anomaly_score"],
            "drift_detected": drift_result["drift_detected"],
            "trust_score": trust_result["trust_score"],
            "status": trust_result["status"],
        })
    except Exception as exc:
        logging.error("Failed to store analysis: %s", exc)
        raise

    try:
        await create_notification(result)
    except Exception as exc:
        logging.error("Failed to create notification: %s", exc)

    return result
