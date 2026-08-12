import asyncio

import pytest

from app.services import analysis_service
from app.services.analysis_service import analyze_device
import app.database as database_module
from app.routes.dashboard_routes import dashboard_summary


class DummyDatabase:
    def __init__(self):
        self.devices = {"test-device": {"device_id": "test-device"}}
        self.analysis = []

    async def get_device(self, device_id):
        return self.devices.get(device_id)

    async def store_analysis(self, analysis):
        self.analysis.append(analysis)
        return "stored"


class DummyNotificationService:
    async def create_notification(self, result):
        self.last = result
        return None


@pytest.mark.asyncio
async def test_complete_analysis_pipeline(monkeypatch):
    dummy_db = DummyDatabase()
    dummy_notifications = DummyNotificationService()

    monkeypatch.setattr(analysis_service, "database", dummy_db)
    monkeypatch.setattr(analysis_service, "create_notification", dummy_notifications.create_notification)

    result = await analyze_device("test-device", {
        "packet_rate": 10.0,
        "behavior_score": 80.0,
        "network_score": 90.0,
        "firmware_score": 95.0,
    })

    assert result["device_id"] == "test-device"
    assert result["trust_score"] >= 0.0
    assert result["status"] in {"TRUSTED", "ANOMALY", "DRIFT"}
    assert dummy_db.analysis


def test_dashboard_summary_mock(monkeypatch):
    fake_summary = {
        "total_devices": 5,
        "trusted_devices": 4,
        "anomaly_devices": 1,
        "drift_devices": 0,
        "total_analysis_today": 6,
        "critical_devices": 0,
    }

    async def fake_get_dashboard_summary():
        return fake_summary

    monkeypatch.setattr(database_module, "get_dashboard_summary", fake_get_dashboard_summary)

    summary = asyncio.run(dashboard_summary())
    assert summary == fake_summary


def test_dashboard_summary_route(client, in_memory_database):
    in_memory_database["devices"]["route-device"] = {
        "device_id": "route-device",
        "device_name": "Route Device",
        "device_type": "sensor",
    }
    response = client.get("/api/dashboard/summary")
    assert response.status_code == 200
    assert response.json()["total_devices"] == 1


def test_dashboard_history_route(monkeypatch, client):
    expected_history = [
        {
            "device_id": "history-device",
            "packet_rate": 10.0,
            "behavior_score": 80.0,
            "network_score": 90.0,
            "firmware_score": 95.0,
            "anomaly_detected": False,
            "anomaly_score": 0.15,
            "drift_detected": False,
            "trust_score": 0.92,
            "status": "TRUSTED",
            "timestamp": "2025-01-01T12:00:00Z",
        }
    ]

    async def fake_get_analysis_history(device_id: str, limit: int = 100):
        return expected_history

    monkeypatch.setattr(database_module, "get_analysis_history", fake_get_analysis_history)

    response = client.get("/api/dashboard/devices/history-device/history")
    assert response.status_code == 200
    assert response.json() == expected_history


def test_dashboard_history_not_found(monkeypatch, client):
    async def fake_get_analysis_history(device_id: str, limit: int = 100):
        return []

    monkeypatch.setattr(database_module, "get_analysis_history", fake_get_analysis_history)

    response = client.get("/api/dashboard/devices/history-device/history")
    assert response.status_code == 404
    assert response.json()["message"] == "No history found for this device"
