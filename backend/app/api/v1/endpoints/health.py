"""
Health check endpoints for monitoring and readiness probes.
"""

from datetime import datetime
from fastapi import APIRouter
from pydantic import BaseModel

from backend.app.core.config import settings

router = APIRouter(tags=["health"])


class HealthResponse(BaseModel):
    """Health check response schema."""
    status: str
    app_name: str
    version: str
    environment: str
    timestamp: str


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Basic health check endpoint.
    Used by load balancers and monitoring systems.
    """
    return HealthResponse(
        status="healthy",
        app_name=settings.app_name,
        version=settings.app_version,
        environment=settings.environment,
        timestamp=datetime.utcnow().isoformat() + "Z",
    )


@router.get("/health/ready")
async def readiness_check() -> dict:
    """
    Readiness probe for Kubernetes/ECS.
    Checks if application is ready to serve traffic.
    """
    # TODO: Add database connectivity check
    return {"status": "ready"}


@router.get("/health/live")
async def liveness_check() -> dict:
    """
    Liveness probe for Kubernetes/ECS.
    Checks if application is alive.
    """
    return {"status": "alive"}
