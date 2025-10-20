"""
Health check endpoints
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from config.database import get_db, check_database_connection
from config.settings import get_settings

router = APIRouter()


@router.get("/health")
async def health_check():
    """
    Health check endpoint
    Returns the health status of the application
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "Smart App API"
    }


@router.get("/health/db")
async def database_health():
    """
    Database health check
    """
    is_healthy = check_database_connection()
    
    return {
        "database": "healthy" if is_healthy else "unhealthy",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/health/detailed")
async def detailed_health(db: Session = Depends(get_db)):
    """
    Detailed health check with all service statuses
    """
    settings = get_settings()
    
    # Check database
    db_healthy = check_database_connection()
    
    # Check Ollama (basic)
    ollama_status = "unknown"
    try:
        import httpx
        response = httpx.get(f"{settings.ollama_base_url}/api/tags", timeout=5)
        ollama_status = "healthy" if response.status_code == 200 else "unhealthy"
    except Exception:
        ollama_status = "unhealthy"
    
    return {
        "status": "healthy" if db_healthy else "degraded",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "database": "healthy" if db_healthy else "unhealthy",
            "ollama": ollama_status,
        },
        "version": settings.app_version
    }

