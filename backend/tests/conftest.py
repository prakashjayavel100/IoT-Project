import asyncio

import pytest
from fastapi.testclient import TestClient

import app.database as database_module
import app.main as app_main


async def _noop_async(*args, **kwargs):
    return None


@pytest.fixture(autouse=True)
def disable_external_startup(monkeypatch):
    """Prevent MQTT and MongoDB and MQTT side effects during tests."""
    monkeypatch.setattr(app_main, "start_mqtt", lambda: None)
    monkeypatch.setattr(app_main.database, "connect_db", _noop_async)
    monkeypatch.setattr(app_main.database, "close_db", _noop_async)

    state = {
        "devices": {},
        "raw_data": [],
        "analysis": [],
        "notifications": [],
    }

    async def get_device(device_id: str):
        return state["devices"].get(device_id)

    async def insert_device(device: dict):
        state["devices"][device["device_id"]] = {**device}
        return device["device_id"]

    async def get_all_devices(limit: int = 100):
        return list(state["devices"].values())[:limit]

    async def delete_device(device_id: str):
        return int(state["devices"].pop(device_id, None) is not None)

    async def insert_raw_device_data(device_id: str, data: dict):
        state["raw_data"].append({"device_id": device_id, **data})
        return len(state["raw_data"])

    async def store_analysis(analysis: dict):
        state["analysis"].append(analysis)
        return len(state["analysis"])

    async def get_dashboard_summary():
        return {
            "total_devices": len(state["devices"]),
            "trusted_devices": len(state["devices"]),
            "anomaly_devices": 0,
            "drift_devices": 0,
            "total_analysis_today": 0,
            "critical_devices": 0,
        }

    async def get_notifications(limit: int = 100):
        return list(reversed(state["notifications"]))[:limit]

    async def get_notifications_for_device(device_id: str, limit: int = 100):
        return [n for n in reversed(state["notifications"]) if n["device_id"] == device_id][:limit]

    monkeypatch.setattr(database_module, "get_device", get_device)
    monkeypatch.setattr(database_module, "insert_device", insert_device)
    monkeypatch.setattr(database_module, "get_all_devices", get_all_devices)
    monkeypatch.setattr(database_module, "delete_device", delete_device)
    monkeypatch.setattr(database_module, "insert_raw_device_data", insert_raw_device_data)
    monkeypatch.setattr(database_module, "store_analysis", store_analysis)
    monkeypatch.setattr(database_module, "get_dashboard_summary", get_dashboard_summary)
    monkeypatch.setattr(database_module, "get_notifications", get_notifications)
    monkeypatch.setattr(database_module, "get_notifications_for_device", get_notifications_for_device)

    return state


@pytest.fixture
def client():
    return TestClient(app_main.app)


@pytest.fixture
def in_memory_database(monkeypatch):
    state = {
        "devices": {},
        "raw_data": [],
        "analysis": [],
        "notifications": [],
    }

    async def get_device(device_id: str):
        return state["devices"].get(device_id)

    async def insert_device(device: dict):
        state["devices"][device["device_id"]] = {**device}
        return device["device_id"]

    async def get_all_devices(limit: int = 100):
        return list(state["devices"].values())[:limit]

    async def delete_device(device_id: str):
        return int(state["devices"].pop(device_id, None) is not None)

    async def insert_raw_device_data(device_id: str, data: dict):
        state["raw_data"].append({"device_id": device_id, **data})
        return len(state["raw_data"])

    async def get_dashboard_summary():
        return {
            "total_devices": len(state["devices"]),
            "trusted_devices": len(state["devices"]),
            "anomaly_devices": 0,
            "drift_devices": 0,
            "total_analysis_today": 0,
            "critical_devices": 0,
        }

    monkeypatch.setattr(app_main.database, "get_device", get_device)
    monkeypatch.setattr(app_main.database, "insert_device", insert_device)
    monkeypatch.setattr(app_main.database, "get_all_devices", get_all_devices)
    monkeypatch.setattr(app_main.database, "delete_device", delete_device)
    monkeypatch.setattr(app_main.database, "insert_raw_device_data", insert_raw_device_data)
    monkeypatch.setattr(app_main.database, "get_dashboard_summary", get_dashboard_summary)

    return state
