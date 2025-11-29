"""
API V1 Router
Central router for all v1 endpoints
"""

from fastapi import APIRouter
from app.api.v1.endpoints import analyze

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(
    analyze.router,
    prefix="/analyze",
    tags=["Analysis"]
)

# Health check for API v1
@api_router.get("/health", tags=["Health"])
async def api_health():
    """
    API v1 health check
    """
    return {
        "status": "healthy",
        "version": "1.0"
    }
