from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)

    # Project details
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    # Who created this project?
    # ForeignKey links this to the users table
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships — lets us do project.owner and project.tasks in Python
    owner = relationship("User", back_populates="projects")
    tasks = relationship("Task", back_populates="project")