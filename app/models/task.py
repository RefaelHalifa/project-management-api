from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum

# Task status options — like a dropdown in the database
class TaskStatus(str, enum.Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"

# Task priority options
class TaskPriority(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)

    # Task details
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)

    # Status and priority use our enums above
    status = Column(Enum(TaskStatus), default=TaskStatus.todo)
    priority = Column(Enum(TaskPriority), default=TaskPriority.medium)

    # Due date — optional
    due_date = Column(DateTime(timezone=True), nullable=True)

    # stores path to uploaded file
    file_path = Column(String, nullable=True)

    # Which project does this task belong to?
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)

    # Who is assigned to this task?
    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    project = relationship("Project", back_populates="tasks")
    assignee = relationship("User", back_populates="assigned_tasks")