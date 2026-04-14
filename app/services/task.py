from sqlalchemy.orm import Session
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate

def get_tasks(db: Session, project_id: int, skip: int = 0, limit: int = 100):
    # Get all tasks belonging to a specific project
    return (
        db.query(Task)
        .filter(Task.project_id == project_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_task(db: Session, task_id: int):
    # Get a single task by ID
    return db.query(Task).filter(Task.id == task_id).first()

def create_task(db: Session, task: TaskCreate):
    # Create a new task in the database
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
    # Get the existing task
    db_task = get_task(db, task_id)
    if not db_task:
        return None

    # Only update fields that were actually sent
    update_data = task.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)

    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int):
    # Get and delete the task
    db_task = get_task(db, task_id)
    if not db_task:
        return None
    db.delete(db_task)
    db.commit()
    return db_task