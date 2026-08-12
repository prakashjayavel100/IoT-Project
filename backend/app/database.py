from typing import Optional, List, Any
from datetime import datetime, timedelta

import certifi
from motor.motor_asyncio import AsyncIOMotorClient


class DatabaseConnectionError(RuntimeError):
    pass

from app.config import settings

# Global client and database handle
client: Optional[AsyncIOMotorClient] = None
db = None


def _ensure_db_connected():
    if client is None or db is None:
        raise DatabaseConnectionError("MongoDB is not connected")


async def connect_db():
    """Create a Motor client and attach the database handle.

    Uses `settings.mongodb_uri` and `settings.DATABASE_NAME` from the environment.
    """
    global client, db
    try:
        client = AsyncIOMotorClient(
            settings.mongodb_uri,
            tls=True,
            tlsCAFile=certifi.where(),
            serverSelectionTimeoutMS=10000,
            connectTimeoutMS=10000,
        )
        # Verify the connection immediately without exposing sensitive details.
        await client.admin.command("ping")
        db = client[settings.DATABASE_NAME]
    except Exception:
        client = None
        db = None
        raise DatabaseConnectionError("Unable to connect to MongoDB")


async def close_db():
    """Close the Motor client connection."""
    global client, db
    if client:
        client.close()
        client = None
    db = None


async def ping_db() -> bool:
    """Ping the MongoDB server to check connectivity.

    Returns True when ping succeeds, False otherwise.
    """
    if client is None:
        return False
    try:
        await client.admin.command('ping')
        return True
    except Exception:
        return False


async def insert_device(device: dict) -> Any:
    """Insert a device document into the `devices` collection.

    The `device` dict should include `device_id`, `device_name` and `device_type`.
    A `created_at` timestamp will be added automatically.
    Returns the inserted id.
    """
    _ensure_db_connected()
    device = device.copy()
    device.setdefault('created_at', datetime.utcnow())
    result = await db['devices'].insert_one(device)
    return result.inserted_id


async def get_device(device_id: str) -> Optional[dict]:
    """Fetch a device document by its `device_id`."""
    _ensure_db_connected()
    return await db['devices'].find_one({'device_id': device_id})


async def get_all_devices(limit: int = 100) -> List[dict]:
    """Return a list of registered devices."""
    _ensure_db_connected()
    cursor = db['devices'].find({}).sort('created_at', -1).limit(limit)
    return await cursor.to_list(length=limit)


async def delete_device(device_id: str) -> int:
    """Delete a device by `device_id`. Returns deleted count."""
    _ensure_db_connected()
    result = await db['devices'].delete_one({'device_id': device_id})
    return result.deleted_count


async def store_analysis(analysis: dict) -> Any:
    """Store an analysis document into `device_analysis` collection.

    Expected keys: device_id, packet_rate, behavior_score, network_score, firmware_score,
    anomaly_detected, anomaly_score, drift_detected, trust_score, status
    """
    _ensure_db_connected()
    doc = analysis.copy()
    doc.setdefault('timestamp', datetime.utcnow())
    result = await db['device_analysis'].insert_one(doc)
    return result.inserted_id


async def insert_raw_device_data(device_id: str, data: dict) -> Any:
    """Store raw input device data in the `raw_device_data` collection."""
    _ensure_db_connected()
    doc = {
        "device_id": device_id,
        "packet_rate": data['packet_rate'],
        "behavior_score": data['behavior_score'],
        "network_score": data['network_score'],
        "firmware_score": data['firmware_score'],
        "timestamp": datetime.utcnow(),
    }
    result = await db['raw_device_data'].insert_one(doc)
    return result.inserted_id


async def get_latest_analysis(device_id: str) -> Optional[dict]:
    """Return the latest analysis document for a device (by timestamp)."""
    _ensure_db_connected()
    cursor = db['device_analysis'].find({'device_id': device_id}).sort('timestamp', -1).limit(1)
    docs = await cursor.to_list(length=1)
    return docs[0] if docs else None


async def get_analysis_history(device_id: str, limit: int = 100) -> List[dict]:
    """Return a list of analysis documents for a device, most-recent first."""
    _ensure_db_connected()
    cursor = db['device_analysis'].find(
        {
            'device_id': device_id,
            'packet_rate': {'$exists': True},
            'behavior_score': {'$exists': True},
            'network_score': {'$exists': True},
            'firmware_score': {'$exists': True},
            'anomaly_detected': {'$exists': True},
            'anomaly_score': {'$exists': True},
            'drift_detected': {'$exists': True},
            'trust_score': {'$exists': True},
            'status': {'$exists': True},
            'timestamp': {'$exists': True},
        }
    ).sort('timestamp', -1).limit(limit)
    return await cursor.to_list(length=limit)


async def get_dashboard_summary() -> dict:
    """Return high-level dashboard counts based on MongoDB data."""
    _ensure_db_connected()
    total_devices = await db['devices'].count_documents({})

    # Build latest analysis per device using aggregation
    pipeline = [
        {"$sort": {"device_id": 1, "timestamp": -1}},
        {
            "$group": {
                "_id": "$device_id",
                "status": {"$first": "$status"},
            }
        }
    ]
    latest_statuses = await db['device_analysis'].aggregate(pipeline).to_list(length=None)

    trusted_devices = sum(1 for doc in latest_statuses if doc.get('status') == 'TRUSTED')
    anomaly_devices = sum(1 for doc in latest_statuses if doc.get('status') == 'ANOMALY')
    drift_devices = sum(1 for doc in latest_statuses if doc.get('status') == 'DRIFT')
    critical_devices = drift_devices

    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    total_analysis_today = await db['device_analysis'].count_documents({
        'timestamp': {'$gte': today}
    })

    return {
        'total_devices': total_devices,
        'trusted_devices': trusted_devices,
        'anomaly_devices': anomaly_devices,
        'drift_devices': drift_devices,
        'total_analysis_today': total_analysis_today,
        'critical_devices': critical_devices,
    }


async def get_dashboard_devices(limit: int = 100) -> List[dict]:
    """Return each device with its latest analysis metadata."""
    pipeline = [
        {
            "$lookup": {
                "from": "device_analysis",
                "let": {"device_id": "$device_id"},
                "pipeline": [
                    {"$match": {"$expr": {"$eq": ["$device_id", "$$device_id"]}}},
                    {"$sort": {"timestamp": -1}},
                    {"$limit": 1},
                ],
                "as": "latest_analysis",
            }
        },
        {"$unwind": {"path": "$latest_analysis", "preserveNullAndEmptyArrays": True}},
        {"$limit": limit},
    ]
    devices = await db['devices'].aggregate(pipeline).to_list(length=limit)

    return [
        {
            'device_id': device.get('device_id'),
            'device_name': device.get('device_name'),
            'device_type': device.get('device_type'),
            'latest_trust_score': device.get('latest_analysis', {}).get('trust_score'),
            'latest_status': device.get('latest_analysis', {}).get('status'),
            'latest_anomaly_result': device.get('latest_analysis', {}).get('anomaly_detected'),
            'latest_drift_result': device.get('latest_analysis', {}).get('drift_detected'),
            'latest_timestamp': device.get('latest_analysis', {}).get('timestamp'),
        }
        for device in devices
    ]


async def store_notification(notification: dict) -> Any:
    """Persist a notification document into the `notifications` collection."""
    _ensure_db_connected()
    doc = notification.copy()
    doc.setdefault('timestamp', datetime.utcnow())
    result = await db['notifications'].insert_one(doc)
    return result.inserted_id


async def get_notifications(limit: int = 100) -> List[dict]:
    """Return a list of notifications, newest first."""
    _ensure_db_connected()
    cursor = db['notifications'].find({}).sort('timestamp', -1).limit(limit)
    return await cursor.to_list(length=limit)


async def get_notifications_for_device(device_id: str, limit: int = 100) -> List[dict]:
    """Return notifications for a specific device."""
    _ensure_db_connected()
    cursor = db['notifications'].find({'device_id': device_id}).sort('timestamp', -1).limit(limit)
    return await cursor.to_list(length=limit)
