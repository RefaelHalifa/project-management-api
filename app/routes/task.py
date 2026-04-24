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

@router.get(
    "/",
    response_model=PaginatedResponse[TaskResponse],
    summary="List tasks for a project",
    description="Get a paginated list of tasks for a specific project. Filter by status, priority or assignee. Sort by any field."
)
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
        db, project_id=project_id, page=page, limit=limit,
        sort=sort, order=order, status=status,
        priority=priority, assignee_id=assignee_id
    )

@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Get a single task",
    description="Get full details of a single task by its ID. Returns 404 if not found."
)
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

@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    description="Create a new task inside a project. If an assignee_id is provided, a background notification is sent automatically."
)
def create_task(
    task: TaskCreate,
    bg_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_task = task_service.create_task(db, task)
    if db_task.assignee_id:
        bg_tasks.add_task(
            background_tasks.notify_task_assigned,
            db_task.id,
            db_task.assignee_id
        )
    return db_task

@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Update a task",
    description="Update any task field. Only send fields you want to change. Changing assignee or status triggers a background notification."
)
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
    if task.assignee_id:
        bg_tasks.add_task(
            background_tasks.notify_task_assigned,
            updated.id, updated.assignee_id
        )
    if task.status:
        bg_tasks.add_task(
            background_tasks.notify_task_status_changed,
            updated.id, updated.status.value
        )
    return updated

@router.delete(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Delete a task",
    description="Permanently delete a task. This action cannot be undone."
)
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