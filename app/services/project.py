from sqlalchemy.orm import Session
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate

def get_projects(db: Session, skip: int = 0, limit: int = 100):
    # Get all projects from the database
    return db.query(Project).offset(skip).limit(limit).all()

def get_project(db: Session, project_id: int):
    # Get a single project by ID
    return db.query(Project).filter(Project.id == project_id).first()

def create_project(db: Session, project: ProjectCreate, owner_id: int):
    # Create a new project in the database
    db_project = Project(
        name=project.name,
        description=project.description,
        owner_id=owner_id
    )
    db.add(db_project)       # Stage the new record
    db.commit()              # Save to database
    db.refresh(db_project)  # Refresh to get generated fields (id, created_at)
    return db_project

def update_project(db: Session, project_id: int, project: ProjectUpdate):
    # Get the existing project
    db_project = get_project(db, project_id)
    if not db_project:
        return None

    # Only update fields that were actually sent
    update_data = project.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_project, field, value)

    db.commit()
    db.refresh(db_project)
    return db_project

def delete_project(db: Session, project_id: int):
    # Get and delete the project
    db_project = get_project(db, project_id)
    if not db_project:
        return None
    db.delete(db_project)
    db.commit()
    return db_project