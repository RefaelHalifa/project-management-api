from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate
from typing import Optional

# Allowed sort fields — prevents SQL injection via sort param
ALLOWED_SORT_FIELDS = {
    "created_at": Project.created_at,
    "updated_at": Project.updated_at,
    "name": Project.name,
}

def get_projects(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    page: int = 1,
    sort: str = "created_at",
    order: str = "desc",
    name: Optional[str] = None,
):
    query = db.query(Project)

    # FILTER — by name (partial match)
    if name:
        query = query.filter(Project.name.ilike(f"%{name}%"))

    # SORT — only allow safe fields
    sort_column = ALLOWED_SORT_FIELDS.get(sort, Project.created_at)
    if order == "asc":
        query = query.order_by(asc(sort_column))
    else:
        query = query.order_by(desc(sort_column))

    # COUNT total before pagination
    total = query.count()

    # PAGINATE — calculate offset from page number
    offset = (page - 1) * limit
    items = query.offset(offset).limit(limit).all()

    # Calculate total pages
    pages = (total + limit - 1) // limit

    return {
        "items": items,
        "total": total,
        "page": page,
        "limit": limit,
        "pages": pages
    }

def get_project(db: Session, project_id: int):
    return db.query(Project).filter(Project.id == project_id).first()

def create_project(db: Session, project: ProjectCreate, owner_id: int):
    db_project = Project(
        name=project.name,
        description=project.description,
        owner_id=owner_id
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def update_project(db: Session, project_id: int, project: ProjectUpdate):
    db_project = get_project(db, project_id)
    if not db_project:
        return None
    update_data = project.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_project, field, value)
    db.commit()
    db.refresh(db_project)
    return db_project

def delete_project(db: Session, project_id: int):
    db_project = get_project(db, project_id)
    if not db_project:
        return None
    db.delete(db_project)
    db.commit()
    return db_project