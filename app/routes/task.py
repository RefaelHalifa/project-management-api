from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.schemas.common import PaginatedResponse
from app.services import task as task_service
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.models.task import TaskStatus, TaskPriority
from app import tasks as background_tasks
from typing import Optional

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("/", response_model=PaginatedResponse[TaskResponse])
def get_tasks(
    project_id: int,
    page: int = 1,
    limit: int = 10,
    sort: str = "created_at",
    order: str = "desc",
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    assignee_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return task_service.get_tasks(
        db,
        project_id=project_id,
        page=page,
        limit=limit,
        sort=sort,
        order=order,
        status=status,
        priority=priority,
        assignee_id=assignee_id
    )

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = task_service.get_task(db, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    return task

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task: TaskCreate,
    bg_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_task = task_service.create_task(db, task)

    # Fire background notification if task is assigned
    if db_task.assignee_id:
        bg_tasks.add_task(
            background_tasks.notify_task_assigned,
            db_task.id,
            db_task.assignee_id
        )

    return db_task

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task: TaskUpdate,
    bg_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    updated = task_service.update_task(db, task_id, task)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )

    # Fire background notification if assignee changed
    if task.assignee_id:
        bg_tasks.add_task(
            background_tasks.notify_task_assigned,
            updated.id,
            updated.assignee_id
        )

    # Fire background notification if status changed
    if task.status:
        bg_tasks.add_task(
            background_tasks.notify_task_status_changed,
            updated.id,
            updated.status.value
        )

    return updated

@router.delete("/{task_id}", response_model=TaskResponse)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    deleted = task_service.delete_task(db, task_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    return deleted