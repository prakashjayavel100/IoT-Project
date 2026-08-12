import argparse
import json
import sys
import time
import urllib.error
import urllib.request


BASE_URL = "http://localhost:8000"


def post_json(path, payload, base_url=BASE_URL):
    url = f"{base_url.rstrip('/')}{path}"
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request) as response:
            text = response.read().decode("utf-8")
            return json.loads(text)
    except urllib.error.HTTPError as exc:
        print(f"ERROR {exc.code} for {url}")
        try:
            print(exc.read().decode("utf-8"))
        except Exception:
            pass
        return None
    except urllib.error.URLError as exc:
        print(f"Could not connect to backend at {url}: {exc.reason}")
        return None


def register_device(device_id, device_name, device_type, base_url=BASE_URL):
    payload = {
        "device_id": device_id,
        "device_name": device_name,
        "device_type": device_type,
    }
    print(f"Registering device: {device_id} ({device_name})")
    response = post_json("/api/devices", payload, base_url)
    if response and response.get("success"):
        print("Device registered successfully.\n")
    else:
        print("Device registration may already exist or failed.\n")
    return response


def send_observation(device_id, payload, base_url=BASE_URL):
    print("-" * 60)
    print(f"Sending data for {device_id}")
    print(json.dumps(payload, indent=2))
    response = post_json(f"/api/devices/{device_id}/analyze", payload, base_url)
    if response is None:
        print("No response from backend.\n")
        return
    print("Backend response:")
    print(json.dumps(response, indent=2))
    print("-" * 60)
    print()
    return response


def demo_sequence(base_url):
    devices = [
        {
            "device_id": "smart-camera-normal",
            "device_name": "Smart Camera Normal",
            "device_type": "camera",
        },
        {
            "device_id": "smart-thermostat-normal",
            "device_name": "Smart Thermostat Normal",
            "device_type": "thermostat",
        },
        {
            "device_id": "smart-camera-abnormal",
            "device_name": "Smart Camera Abnormal",
            "device_type": "camera",
        },
        {
            "device_id": "smart-camera-drift",
            "device_name": "Smart Camera Drift",
            "device_type": "camera",
        },
    ]

    print("Simulating IoT data for backend analysis.\n")
    for device in devices:
        register_device(device["device_id"], device["device_name"], device["device_type"], base_url)

    print("\n1) NORMAL behavior for normal smart camera")
    normal_camera_payloads = [
        {"packet_rate": 10.0, "behavior_score": 88.0, "network_score": 92.0, "firmware_score": 96.0},
        {"packet_rate": 11.0, "behavior_score": 87.0, "network_score": 91.0, "firmware_score": 96.5},
    ]
    for payload in normal_camera_payloads:
        send_observation("smart-camera-normal", payload, base_url)
        time.sleep(0.5)

    print("\n2) NORMAL behavior for normal smart thermostat")
    thermostat_payloads = [
        {"packet_rate": 4.0, "behavior_score": 90.0, "network_score": 93.0, "firmware_score": 98.0},
        {"packet_rate": 4.5, "behavior_score": 89.0, "network_score": 92.0, "firmware_score": 98.0},
    ]
    for payload in thermostat_payloads:
        send_observation("smart-thermostat-normal", payload, base_url)
        time.sleep(0.5)

    print("\n3) ANOMALY behavior for abnormal smart camera")
    send_observation(
        "smart-camera-abnormal",
        {"packet_rate": 10.0, "behavior_score": 88.0, "network_score": 92.0, "firmware_score": 96.0},
        base_url,
    )
    time.sleep(0.5)
    send_observation(
        "smart-camera-abnormal",
        {"packet_rate": 80.0, "behavior_score": 20.0, "network_score": 30.0, "firmware_score": 70.0},
        base_url,
    )

    print("\n4) DRIFT behavior for camera showing gradual change")
    drift_payloads = [
        {"packet_rate": 10.0, "behavior_score": 88.0, "network_score": 92.0, "firmware_score": 96.0},
        {"packet_rate": 10.5, "behavior_score": 84.0, "network_score": 90.0, "firmware_score": 95.0},
        {"packet_rate": 11.0, "behavior_score": 78.0, "network_score": 86.0, "firmware_score": 94.0},
        {"packet_rate": 12.0, "behavior_score": 70.0, "network_score": 80.0, "firmware_score": 92.0},
    ]
    for payload in drift_payloads:
        send_observation("smart-camera-drift", payload, base_url)
        time.sleep(0.5)

    print("Demo complete. The backend computed anomaly, drift, trust score, and status for each payload.")


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Simple IoT simulator for the IoT trust drift backend demo."
    )
    parser.add_argument(
        "--url",
        default=BASE_URL,
        help="Backend base URL, e.g. http://localhost:8000",
    )
    args = parser.parse_args(argv)

    demo_sequence(args.url)


if __name__ == "__main__":
    main()
