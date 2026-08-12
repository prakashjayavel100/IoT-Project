# IoT Trust Drift Detection Backend

This repository contains the backend scaffold for the "IoT Trust Drift Detection System for Secure Device Monitoring" hackathon project.

## What's included

- FastAPI application
- Basic routes and placeholders for services (anomaly, drift, trust)
- MongoDB (Motor) placeholder connection
- MQTT client placeholder (paho-mqtt)

## Install

Create a virtual environment and install dependencies:

```bash
python -m venv .venv
# Activate on Windows (PowerShell):
.venv\Scripts\Activate.ps1
# Or on Windows (cmd):
.venv\Scripts\activate.bat
# On macOS / Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

## Configuration

Copy `.env.example` to `.env` and set values for the following environment variables:

- `MONGODB_URI`: MongoDB connection string (Atlas or local).
- `DATABASE_NAME`: Database name to store device data.
- `MQTT_BROKER`: Hostname or IP of MQTT broker.
- `MQTT_PORT`: MQTT broker port (usually 1883).
- `MQTT_USERNAME`: MQTT username (if required).
- `MQTT_PASSWORD`: MQTT password (if required).
- `MQTT_TOPIC`: MQTT topic to subscribe to device data.

Do NOT hardcode credentials directly in code; use `.env`.

## Run

From the `backend` folder run:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Test health endpoint

Open a browser or use `curl`:

```bash
curl http://localhost:8000/health
```

## Next steps

Implement feature extraction, anomaly detection (Isolation Forest), ADWIN drift detection (river), and device trust scoring logic.
