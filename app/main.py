from fastapi import FastAPI
from app.config import settings

# Create the FastAPI application instance
# title and version automatically appear in your Swagger UI
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="A full-featured Project Management REST API"
)

# Root endpoint — acts as a basic health check
@app.get("/", tags=["Health"])
def root():
    return {
        "app": settings.app_name,
        "version": settings.app_version,
        "status": "running"
    }