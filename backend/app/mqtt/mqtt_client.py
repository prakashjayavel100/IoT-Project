import json
import logging
import threading
from typing import Dict, Any

import paho.mqtt.client as mqtt

from app.config import settings
from app.services.analysis_service import analyze_device

logger = logging.getLogger(__name__)


def _parse_payload(payload: bytes) -> Dict[str, Any]:
    try:
        data = json.loads(payload.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON payload: {exc}")

    required_fields = [
        "device_id",
        "packet_rate",
        "behavior_score",
        "network_score",
        "firmware_score",
    ]
    missing = [field for field in required_fields if field not in data]
    if missing:
        raise ValueError(f"Missing required field(s): {', '.join(missing)}")

    return data


def _on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info("Connected to MQTT broker")
        client.subscribe(settings.MQTT_TOPIC)
        logger.info("Subscribed to topic %s", settings.MQTT_TOPIC)
    else:
        logger.error("MQTT connection failed with result code %s", rc)


def _on_message(client, userdata, msg):
    logger.info("MQTT message received on topic %s", msg.topic)
    try:
        payload = _parse_payload(msg.payload)
        device_id = payload["device_id"]
        input_data = {
            "packet_rate": payload["packet_rate"],
            "behavior_score": payload["behavior_score"],
            "network_score": payload["network_score"],
            "firmware_score": payload["firmware_score"],
        }
        threading.Thread(
            target=_run_analysis, args=(device_id, input_data), daemon=True
        ).start()
    except Exception as exc:
        logger.error("Failed to process MQTT message: %s", exc)


def _run_analysis(device_id: str, input_data: Dict[str, Any]):
    try:
        import asyncio

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(analyze_device(device_id, input_data))
        logger.info("MQTT analysis completed for %s: %s", device_id, result)
    except Exception as exc:
        logger.error("MQTT analysis failed for %s: %s", device_id, exc)
    finally:
        try:
            loop.close()
        except Exception:
            pass


def create_mqtt_client(client_id: str = "iot_backend") -> mqtt.Client:
    client_kwargs = {"client_id": client_id}
    if hasattr(mqtt, "CallbackAPIVersion"):
        client_kwargs["callback_api_version"] = mqtt.CallbackAPIVersion.VERSION1

    client = mqtt.Client(**client_kwargs)
    if settings.MQTT_USERNAME and settings.MQTT_PASSWORD:
        client.username_pw_set(
            settings.MQTT_USERNAME,
            settings.MQTT_PASSWORD.get_secret_value(),
        )
    client.on_connect = _on_connect
    client.on_message = _on_message
    return client


def start_mqtt():
    client = create_mqtt_client()
    try:
        client.connect(settings.MQTT_BROKER, settings.MQTT_PORT, keepalive=60)
    except Exception as exc:
        logger.error("Could not connect to MQTT broker: %s", exc)
        return None

    thread = threading.Thread(target=client.loop_forever, daemon=True)
    thread.start()
    logger.info("MQTT client started")
    return client
