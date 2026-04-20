import time
from app.models.task import Task
from sqlalchemy.orm import Session

def notify_task_assigned(task_id: int, assignee_id: int):
    """
    Background job that fires when a task is assigned to a user.
    In production this would send a real email or push notification.
    For now we simulate it with a print and a delay.
    """
    # Simulate sending a notification (e.g. email)
    print(f"\n🔔 BACKGROUND JOB STARTED")
    print(f"   Task {task_id} assigned to user {assignee_id}")
    time.sleep(2)  # Simulate network delay of sending email
    print(f"   ✅ Notification sent to user {assignee_id} for task {task_id}")
    print(f"🔔 BACKGROUND JOB COMPLETE\n")

def notify_task_status_changed(task_id: int, new_status: str):
    """
    Background job that fires when a task status changes.
    """
    print(f"\n🔔 BACKGROUND JOB STARTED")
    print(f"   Task {task_id} status changed to {new_status}")
    time.sleep(1)
    print(f"   ✅ Status change notification sent for task {task_id}")
    print(f"🔔 BACKGROUND JOB COMPLETE\n")