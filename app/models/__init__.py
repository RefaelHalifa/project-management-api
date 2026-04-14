# Import all models here so SQLAlchemy can resolve relationships
# between them. Order matters — User first, then Project, then Task.
from app.models.user import User
from app.models.project import Project
from app.models.task import Task