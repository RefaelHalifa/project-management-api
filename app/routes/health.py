from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime
from app.database import get_db

router = APIRouter()

# Record the moment the app started (module-level, set once)
START_TIME = datetime.utcnow()


@router.get("/health", tags=["Health"])
def health_check(db: Session = Depends(get_db)):
    """
    Actuator endpoint — returns live system status.
    Used by monitoring tools, Docker, and load balancers.
    """

    # Calculate how many seconds the app has been running
    uptime_seconds = (datetime.utcnow() - START_TIME).seconds

    # Try to ping the database with a minimal query
    try:
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception:
        db_status = "disconnected"

    # Overall status: only healthy if DB is reachable
    overall = "healthy" if db_status == "connected" else "degraded"

    return {
        "status": overall,
        "database": db_status,
        "uptime_seconds": uptime_seconds,
        "version": "1.0.0"
    }