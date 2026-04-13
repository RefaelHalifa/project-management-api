from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    # Primary key — unique ID for every user
    id = Column(Integer, primary_key=True, index=True)

    # User details
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)

    # Is this user active or disabled?
    is_active = Column(Boolean, default=True)

    # Timestamps — set automatically by the database
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    projects = relationship("Project", back_populates="owner")
    assigned_tasks = relationship("Task", back_populates="assignee")