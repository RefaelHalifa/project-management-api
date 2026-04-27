from fastapi import FastAPI
from fastapi.security import HTTPBearer
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import SQLAlchemyError
from app.config import settings
from app.exceptions import (
    http_exception_handler,
    validation_error_handler,
    database_error_handler,
    internal_server_error_handler
)
import app.models
from app.routes import project as project_router
from app.routes import task as task_router
from app.routes import auth as auth_router
from app.routes import file as file_router
from app.routes import health as health_router

security = HTTPBearer()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="""
## Project Management API

A full-featured REST API for managing projects and tasks.

### Features
- 🔐 JWT Authentication — secure register and login
- 📋 Projects — create and manage projects
- ✅ Tasks — create tasks with status, priority and due dates
- 🔍 Filter, Pagination, Sort — on all list endpoints
- 📎 File Uploads — attach files to tasks with presigned links
- 🔔 Background Jobs — async notifications on task assignment
    """,
    contact={
        "name": "Rafael Halifa",
        "email": "rafael@test.com"
    },
    license_info={
        "name": "MIT"
    }
)

# Register global exception handlers
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_error_handler)
app.add_exception_handler(SQLAlchemyError, database_error_handler)
app.add_exception_handler(Exception, internal_server_error_handler)

# Register all routers
app.include_router(auth_router.router)
app.include_router(project_router.router)
app.include_router(task_router.router)
app.include_router(file_router.router)
app.include_router(health_router.router)

@app.get("/", tags=["Health"])
def root():
    return {
        "app": settings.app_name,
        "version": settings.app_version,
        "status": "running"
    }