from datetime import datetime
from typing import Dict

from app import database


async def create_notification(result: Dict[str, object]) -> None:
    """Create and store a notification based on analysis result."""
    status = result.get("status")
    if status == "TRUSTED":
        return

    event_type = "ANOMALY" if status == "ANOMALY" else "DRIFT"
    description = (
        "An anomaly was detected in device behavior." if status == "ANOMALY"
        else "A behavior drift was detected for this device."
    )
    level = "warning" if status == "ANOMALY" else "critical"

    notification = {
        "device_id": result["device_id"],
        "status": status,
        "event_type": event_type,
        "description": description,
        "trust_score": result["trust_score"],
        "message": description,
        "level": level,
        "timestamp": datetime.utcnow(),
    }
    await database.store_notification(notification)
