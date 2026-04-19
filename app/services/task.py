from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from app.models.task import Task, TaskStatus, TaskPriority
from app.schemas.task import TaskCreate, TaskUpdate
from typing import Optional

# Allowed sort fields — prevents SQL injection
ALLOWED_SORT_FIELDS = {
    "created_at": Task.created_at,
    "updated_at": Task.updated_at,
    "due_date": Task.due_date,
    "priority": Task.priority,
    "title": Task.title,
}

def get_tasks(
    db: Session,
    project_id: int,
    page: int = 1,
    limit: int = 10,
    sort: str = "created_at",
    order: str = "desc",
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    assignee_id: Optional[int] = None,
):
    query = db.query(Task).filter(Task.project_id == project_id)

    # FILTER — by status
    if status:
        query = query.filter(Task.status == status)

    # FILTER — by priority
    if priority:
        query = query.filter(Task.priority == priority)

    # FILTER — by assignee
    if assignee_id:
        query = query.filter(Task.assignee_id == assignee_id)

    # SORT
    sort_column = ALLOWED_SORT_FIELDS.get(sort, Task.created_at)
    if order == "asc":
        query = query.order_by(asc(sort_column))
    else:
        query = query.order_by(desc(sort_column))

    # COUNT total before pagination
    total = query.count()

    # PAGINATE
    offset = (page - 1) * limit
    items = query.offset(offset).limit(limit).all()

    # Calculate total pages
    pages = (total + limit - 1) // limit

    return {
        "items": items,
        "total": total,
        "page": page,
        "limit": limit,
        "pages": pages
    }

def get_task(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()

def create_task(db: Session, task: TaskCreate):
    db_task = Task(
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        due_date=task.due_date,
        project_id=task.project_id,
        assignee_id=task.assignee_id
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, task_id: int, task: TaskUpdate):
    db_task = get_task(db, task_id)
    if not db_task:
        return None
    update_data = task.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int):
    db_task = get_task(db, task_id)
    if not db_task:
        return None
    db.delete(db_task)
    db.commit()
    return db_task