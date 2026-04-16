from fastapi import FastAPI
from fastapi.security import HTTPBearer
from app.config import settings
import app.models
from app.routes import project as project_router
from app.routes import task as task_router
from app.routes import auth as auth_router

# This adds the Bearer token input to Swagger UI
security = HTTPBearer()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="A full-featured Project Management REST API",
)

# Register all routers
app.include_router(auth_router.router)
app.include_router(project_router.router)
app.include_router(task_router.router)

@app.get("/", tags=["Health"])
def root():
    return {
        "app": settings.app_name,
        "version": settings.app_version,
        "status": "running"
    }