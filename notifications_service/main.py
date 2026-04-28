from fastapi import FastAPI
from pydantic import BaseModel
import logging

# Set up logging so we can see notifications arrive in Docker logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Notifications Service", version="1.0.0")


# The shape of a notification payload we expect to receive
class NotificationPayload(BaseModel):
    user_id: int
    task_id: int
    message: str


@app.get("/health", tags=["Health"])
def health():
    """Health check for this microservice"""
    return {"status": "healthy", "service": "notifications"}


@app.post("/notify", tags=["Notifications"])
def send_notification(payload: NotificationPayload):
    """
    Receive a notification request from the main app.
    In a real system this would send an email, SMS, or push notification.
    For now we log it — proving the inter-service communication works.
    """
    logger.info(
        f"🔔 NOTIFICATION | user_id={payload.user_id} | "
        f"task_id={payload.task_id} | message='{payload.message}'"
    )

    return {
        "status": "sent",
        "user_id": payload.user_id,
        "task_id": payload.task_id,
        "message": payload.message
    }