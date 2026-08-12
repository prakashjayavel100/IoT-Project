import logging

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.routes import health_routes, device_routes, analysis_routes
from app.routes.notification_routes import router as notification_routes
from app.routes.dashboard_routes import router as dashboard_routes
from app.schemas.device_schema import RootResponse
from app import database
from app.database import DatabaseConnectionError
from app.mqtt.mqtt_client import start_mqtt

app = FastAPI(
    title="IoT Trust Drift Detection Backend",
    description="Backend API for an IoT trust, anomaly, and drift detection system.",
    version="1.0.0",
)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://iot-project-bdsg.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1)(:[0-9]+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Invalid request data",
            "errors": exc.errors(),
        },
    )


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"success": False, "message": str(exc)},
    )


@app.exception_handler(DatabaseConnectionError)
async def db_connection_exception_handler(request: Request, exc: DatabaseConnectionError):
    return JSONResponse(
        status_code=503,
        content={"success": False, "message": "Database connection unavailable"},
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "message": exc.detail},
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logging.error("Unhandled exception: %s", exc, exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"success": False, "message": "Internal server error"},
    )


# Include routers
app.include_router(health_routes.router)
app.include_router(device_routes.router)
app.include_router(analysis_routes.router, prefix="/analysis")
app.include_router(notification_routes)
app.include_router(dashboard_routes)


# Lifespan events to connect/disconnect DB
@app.on_event("startup")
async def startup_event():
    try:
        await database.connect_db()
    except DatabaseConnectionError as exc:
        logging.error("MongoDB startup failure: %s", exc)

    # Start MQTT in the background if broker is available.
    start_mqtt()


@app.on_event("shutdown")
async def shutdown_event():
    await database.close_db()


# Simple root
@app.get(
    "/",
    response_model=RootResponse,
    summary="Service root",
    description="Return a brief service description for the API root.",
)
async def root():
    return {"message": "IoT Trust Drift Detection Backend"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
