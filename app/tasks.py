import httpx
import logging

logger = logging.getLogger(__name__)

# The notifications service URL — uses Docker Compose service name as hostname
NOTIFICATIONS_SERVICE_URL = "http://notifications:8001"


def notify_task_assigned(task_id: int, assignee_id: int):
    """
    Background job that fires when a task is assigned to a user.
    Makes a real HTTP call to the notifications microservice.
    """
    try:
        response = httpx.post(
            f"{NOTIFICATIONS_SERVICE_URL}/notify",
            json={
                "user_id": assignee_id,
                "task_id": task_id,
                "message": f"Task {task_id} has been assigned to you."
            },
            timeout=5.0  # don't wait forever if service is down
        )
        logger.info(f"Notification sent: {response.json()}")

    except httpx.RequestError as e:
        # If notifications service is down, log it but don't crash the main app
        # This is a key microservices principle — services fail independently
        logger.error(f"Could not reach notifications service: {e}")


def notify_task_status_changed(task_id: int, new_status: str):
    """
    Background job that fires when a task status changes.
    """
    try:
        response = httpx.post(
            f"{NOTIFICATIONS_SERVICE_URL}/notify",
            json={
                "user_id": 0,  # 0 = broadcast, no specific user
                "task_id": task_id,
                "message": f"Task {task_id} status changed to '{new_status}'."
            },
            timeout=5.0
        )
        logger.info(f"Status notification sent: {response.json()}")

    except httpx.RequestError as e:
        logger.error(f"Could not reach notifications service: {e}")