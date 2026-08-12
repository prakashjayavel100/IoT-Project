import pytest


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_device_registration_and_retrieval(client):
    payload = {"device_id": "device-001", "device_name": "Test Device", "device_type": "sensor"}
    response = client.post("/api/devices", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["device"]["device_id"] == payload["device_id"]
    assert body["device"]["device_name"] == payload["device_name"]

    get_response = client.get(f"/api/devices/{payload['device_id']}")
    assert get_response.status_code == 200
    assert get_response.json()["device_id"] == payload["device_id"]


def test_duplicate_device_registration(client):
    payload = {"device_id": "device-duplicate", "device_name": "Duplicate Device", "device_type": "sensor"}
    first = client.post("/api/devices", json=payload)
    assert first.status_code == 200

    second = client.post("/api/devices", json=payload)
    assert second.status_code == 409
    assert "Device with this device_id already exists" in second.json()["message"]


@pytest.mark.parametrize(
    "payload",
    [
        {"device_id": "device-002", "device_name": "Bad Device"},
        {"device_name": "Missing ID", "device_type": "sensor"},
        {"device_id": "device-003", "device_type": "sensor"},
    ],
)
def test_device_registration_invalid_payload(client, payload):
    response = client.post("/api/devices", json=payload)
    assert response.status_code == 422


@pytest.mark.parametrize(
    "payload",
    [
        {"packet_rate": -1, "behavior_score": 50, "network_score": 50, "firmware_score": 50},
        {"packet_rate": 10, "behavior_score": 150, "network_score": 50, "firmware_score": 50},
        {"packet_rate": 10, "behavior_score": 50, "network_score": -5, "firmware_score": 50},
    ],
)
def test_iot_data_validation(client, payload):
    device_payload = {"device_id": "device-validation", "device_name": "Validation Device", "device_type": "sensor"}
    client.post("/api/devices", json=device_payload)
    response = client.post(f"/api/devices/{device_payload['device_id']}/analyze", json=payload)
    assert response.status_code == 422
