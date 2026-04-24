from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from app.schemas.common import PaginatedResponse
from app.services import project as project_service
from app.auth.dependencies import get_current_user
from app.models.user import User
from typing import Optional

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.get(
    "/",
    response_model=PaginatedResponse[ProjectResponse],
    summary="List all projects",
    description="Get a paginated list of all projects. Supports filtering by name, sorting by any field, and pagination."
)
def get_projects(
    page: int = 1,
    limit: int = 10,
    sort: str = "created_at",
    order: str = "desc",
    name: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return project_service.get_projects(
        db, page=page, limit=limit, sort=sort, order=order, name=name
    )

@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Get a single project",
    description="Get full details of a single project by its ID. Returns 404 if not found."
)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    project = project_service.get_project(db, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} not found"
        )
    return project

@router.post(
    "/",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new project",
    description="Create a new project. The authenticated user becomes the owner automatically."
)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return project_service.create_project(db, project, owner_id=current_user.id)

@router.put(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Update a project",
    description="Update a project's name or description. Only send the fields you want to change — other fields remain unchanged."
)
def update_project(
    project_id: int,
    project: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    updated = project_service.update_project(db, project_id, project)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} not found"
        )
    return updated

@router.delete(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Delete a project",
    description="Permanently delete a project and all its associated tasks. This action cannot be undone."
)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    deleted = project_service.delete_project(db, project_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} not found"
        )
    return deleted