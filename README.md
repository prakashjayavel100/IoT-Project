# IoT Trust & Drift Detection System

An IoT device monitoring and analysis platform that evaluates device
behavior, detects anomalies and drift, and calculates a trust score from
device telemetry.

The project provides a React + Vite frontend and a FastAPI backend
connected to MongoDB. It is designed to make IoT device behavior easier
to monitor, analyze, and understand through a web dashboard.

## 🚀 Live Project

### Frontend

https://iot-project-bdsg.onrender.com

### Backend API

https://iot-trust-backend.onrender.com

### Backend Health Check

https://iot-trust-backend.onrender.com/health

> Note: The live services may take a short time to wake up when using
> free hosting.

------------------------------------------------------------------------

## 🎯 Project Objective

The main goal of this project is to provide a simple IoT device trust
and security monitoring system.

The system can:

-   Register IoT devices
-   Monitor device-related input features
-   Analyze device behavior
-   Detect anomalies
-   Detect behavioral drift
-   Calculate a device trust score
-   Display device status and analysis results
-   Maintain analysis history
-   Generate notifications for important events
-   Provide dashboard-level device statistics

------------------------------------------------------------------------

## 🧠 How the System Works

The basic workflow is:

``` text
                 IoT Device Data
                        │
                        ▼
              React Web Application
                        │
                        ▼
                 FastAPI Backend
                        │
             ┌──────────┴──────────┐
             ▼                     ▼
        MongoDB Database      ML Analysis
                                   │
                    ┌──────────────┼──────────────┐
                    ▼              ▼              ▼
                Anomaly          Drift        Trust Score
                Detection      Detection       Calculation
                    │              │              │
                    └──────────────┼──────────────┘
                                   ▼
                           Analysis Result
                                   │
                                   ▼
                            React Dashboard
```

------------------------------------------------------------------------

## ✨ Main Features

### 1. Device Registration

Users can register an IoT device using:

-   Device ID
-   Device Name
-   Device Type

Example:

``` text
Device ID: DEMO001
Device Name: Smart Camera Demo
Device Type: smart_camera
```

------------------------------------------------------------------------

### 2. Device Analysis

The system accepts device behavior features such as:

``` text
Packet Rate
Behavior Score
Network Score
Firmware Score
```

These values are sent to the backend for analysis.

Example:

``` json
{
  "packet_rate": 25,
  "behavior_score": 0.90,
  "network_score": 0.85,
  "firmware_score": 0.95
}
```

The backend returns an analysis result containing:

-   Anomaly status
-   Anomaly score
-   Drift status
-   Trust score
-   Overall device status
-   Timestamp

------------------------------------------------------------------------

### 3. Anomaly Detection

The system analyzes device behavior and identifies unusual behavior.

Possible result:

``` text
Status: ANOMALY
Anomaly: Detected
```

------------------------------------------------------------------------

### 4. Drift Detection

The system checks whether device behavior is changing from its expected
behavior over time.

Example:

``` text
Drift: Stable
```

or

``` text
Drift: Detected
```

------------------------------------------------------------------------

### 5. Trust Score

A trust score represents the current level of confidence in the device
based on its analyzed behavior.

Example:

``` text
Trust Score: 0.44
```

A healthier device input should generally produce a better trust score
than suspicious or anomalous behavior.

------------------------------------------------------------------------

### 6. Dashboard

The dashboard provides an overview of:

-   Total devices
-   Trusted devices
-   Anomalous devices
-   Drift devices
-   Analysis count
-   Critical devices
-   Latest device status

------------------------------------------------------------------------

### 7. Analysis History

The system can retrieve previous analysis results for a device.

This makes it possible to observe how device behavior changes over time.

------------------------------------------------------------------------

### 8. Notifications

The system provides notification information related to device events,
including:

-   Device ID
-   Status
-   Event type
-   Description
-   Trust score
-   Severity level
-   Message
-   Timestamp

------------------------------------------------------------------------

## 🛠️ Technology Stack

### Frontend

-   React
-   TypeScript
-   Vite
-   Axios
-   React Router

### Backend

-   Python
-   FastAPI
-   Uvicorn
-   Pydantic
-   Python-dotenv

### Database

-   MongoDB
-   Motor / PyMongo

### Machine Learning / Analysis

-   River
-   Scikit-learn
-   NumPy
-   SciPy

### IoT Communication

-   MQTT
-   Paho MQTT

### Deployment

-   GitHub
-   Render

------------------------------------------------------------------------

## 📁 Project Structure

The project is organized into frontend and backend components.

``` text
IoT-Project/
│
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   ├── components/
│   │   ├── api.ts
│   │   └── ...
│   ├── package.json
│   └── vite.config.*
│
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   │   ├── health_routes.py
│   │   │   ├── device_routes.py
│   │   │   └── analysis_routes.py
│   │   ├── mqtt/
│   │   ├── database.py
│   │   └── main.py
│   └── requirements.txt
│
└── README.md
```

> Folder names can vary slightly depending on the local project
> structure.

------------------------------------------------------------------------

# ⚙️ Local Setup

## Prerequisites

Install:

-   Git
-   Node.js
-   Python
-   MongoDB / MongoDB Atlas

------------------------------------------------------------------------

## 1. Clone the Repository

``` bash
git clone https://github.com/prakashjayavel100/IoT-Project.git
cd IoT-Project
```

------------------------------------------------------------------------

# 🔵 Backend Setup

Open a terminal in the backend folder:

``` bash
cd backend
```

Create a virtual environment:

### Windows

``` bash
python -m venv .venv
```

Activate it:

``` bash
.venv\Scripts\activate
```

Install dependencies:

``` bash
pip install -r requirements.txt
```

Run the FastAPI server:

``` bash
uvicorn app.main:app --reload --port 8003
```

Backend should be available at:

``` text
http://127.0.0.1:8003
```

Health check:

``` text
http://127.0.0.1:8003/health
```

------------------------------------------------------------------------

# 🟢 Frontend Setup

Open another terminal:

``` bash
cd frontend
```

Install dependencies:

``` bash
npm install
```

Create a `.env` file:

``` env
VITE_API_BASE_URL=http://127.0.0.1:8003
```

Start the development server:

``` bash
npm run dev
```

Vite will provide a local frontend URL, normally similar to:

``` text
http://localhost:5173
```

------------------------------------------------------------------------

# 🔐 Environment Variables

## Frontend

For local development:

``` env
VITE_API_BASE_URL=http://127.0.0.1:8003
```

For Render:

``` env
VITE_API_BASE_URL=https://iot-trust-backend.onrender.com
```

Do not commit secret keys, database passwords, or private credentials to
GitHub.

------------------------------------------------------------------------

## Backend

The backend requires its database and other environment-specific
configuration to be supplied through environment variables.

Use a local `.env` file for development and Render Environment Variables
for production.

Example:

``` env
MONGODB_URI=your_mongodb_connection_string
```

Use the variable names already expected by the backend code.

------------------------------------------------------------------------

# 🔌 API Endpoints

## Health

``` http
GET /health
```

Example response:

``` json
{
  "status": "ok"
}
```

## List Devices

``` http
GET /api/devices
```

## Get Device

``` http
GET /api/devices/{device_id}
```

## Register Device

``` http
POST /api/devices
```

Example request:

``` json
{
  "device_id": "DEMO001",
  "device_name": "Smart Camera Demo",
  "device_type": "smart_camera"
}
```

## Analyze Device

``` http
POST /api/devices/{device_id}/analyze
```

Example request:

``` json
{
  "packet_rate": 25,
  "behavior_score": 0.90,
  "network_score": 0.85,
  "firmware_score": 0.95
}
```

## Dashboard Summary

``` http
GET /api/dashboard/summary
```

## Dashboard Devices

``` http
GET /api/dashboard/devices
```

## Device History

``` http
GET /api/dashboard/devices/{device_id}/history
```

## Notifications

``` http
GET /api/notifications
```

------------------------------------------------------------------------

# 🧪 Example Device Analysis

Select:

``` text
Smart Camera Demo
Device ID: DEMO001
```

Enter device telemetry:

``` text
Packet Rate:     25
Behavior Score:  0.90
Network Score:   0.85
Firmware Score:  0.95
```

Click:

``` text
Analyze Device
```

The application displays:

``` text
Status
Trust Score
Anomaly
Drift
Anomaly Score
Timestamp
```

------------------------------------------------------------------------

# 🌐 Deployment

The application is deployed using Render.

## Backend

The backend is deployed as a Render Web Service.

Start command:

``` bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## Frontend

The frontend is deployed as a Render Static Site.

Build command:

``` bash
npm install && npm run build
```

Publish directory:

``` text
dist
```

The frontend uses:

``` env
VITE_API_BASE_URL=https://iot-trust-backend.onrender.com
```

------------------------------------------------------------------------

# 🔒 CORS Configuration

Since the frontend and backend are deployed separately, the FastAPI
backend must allow requests from the frontend domain.

Example:

``` python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://iot-project-bdsg.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

------------------------------------------------------------------------

# 📊 Example Analysis Result

A device analysis may return information similar to:

``` json
{
  "device_id": "DEMO001",
  "anomaly_detected": true,
  "anomaly_score": -0.0479,
  "drift_detected": false,
  "trust_score": 0.44,
  "status": "ANOMALY"
}
```

The exact result depends on the device input and analysis state.

------------------------------------------------------------------------

# 🔄 Application Flow

``` text
1. User opens the web application
              ↓
2. Dashboard loads registered devices
              ↓
3. User selects an IoT device
              ↓
4. User enters device telemetry
              ↓
5. Frontend sends data using Axios
              ↓
6. FastAPI receives the request
              ↓
7. Analysis logic evaluates the device
              ↓
8. MongoDB stores/retrieves device data
              ↓
9. Backend returns analysis result
              ↓
10. Frontend displays trust, anomaly and drift
```

------------------------------------------------------------------------

# 🏆 Use Cases

This project can be used for:

-   IoT device monitoring
-   Smart camera monitoring
-   IoT security analysis
-   Device trust evaluation
-   Anomaly detection
-   Behavioral drift monitoring
-   Smart city IoT environments
-   Security-focused IoT dashboards

------------------------------------------------------------------------

# 🔮 Future Improvements

Possible future enhancements include:

-   Real-time IoT sensor integration
-   Advanced anomaly detection models
-   Improved trust-score calculation
-   Real-time MQTT telemetry visualization
-   Device risk classification
-   Email/SMS alerts
-   Authentication and role-based access
-   More detailed analytics and charts
-   Containerized deployment using Docker

------------------------------------------------------------------------

# 👨‍💻 Project

**IoT Trust & Drift Detection System**

Built using:

``` text
React + TypeScript + FastAPI + MongoDB + Machine Learning + MQTT
```

Deployed using:

``` text
GitHub + Render
```

------------------------------------------------------------------------

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on
GitHub.
