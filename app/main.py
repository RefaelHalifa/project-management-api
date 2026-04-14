from fastapi import FastAPI
from app.config import settings
import app.models
from app.routes import project as project_router
from app.routes import task as task_router

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="A full-featured Project Management REST API"
)

# Register routes — this is where FastAPI learns about our endpoints
app.include_router(project_router.router)
app.include_router(task_router.router)

# Root health check endpoint
@app.get("/", tags=["Health"])
def root():
    return {
        "app": settings.app_name,
        "version": settings.app_version,
        "status": "running"
    }