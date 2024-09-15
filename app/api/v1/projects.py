from datetime import date
from fastapi import APIRouter, Depends, HTTPException,Query
from typing import List
from app.models.project import Project as ProjectModel
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate
from app.db.session import get_db
from sqlalchemy.orm import Session
from typing import Optional

router = APIRouter()

@router.post("/", response_model=ProjectResponse)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    db_project = ProjectModel(
        name=project.name,
        description=project.description,
        active=project.active,
        created_by=project.created_by,
        created_at=date.today(),
        updated_at=date.today()
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

@router.get("/", response_model=List[ProjectResponse])
def read_projects(
    page: int = Query(1, gt=0),
    size: int = Query(10, gt=0),
    sort: str = Query("name"),
    direction: str = Query("asc"),
    active: Optional[bool] = None,  # Optional filter parameter
    db: Session = Depends(get_db)
):
    # Validate the sort direction
    if direction not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Sort direction must be 'asc' or 'desc'")
    
    # Calculate offset for pagination
    offset = (page - 1) * size

    # Create the sorting order
    sort_column = getattr(ProjectModel, sort, None)
    if not sort_column:
        raise HTTPException(status_code=400, detail="Invalid sort field")
    
    if direction == "asc":
        projects_query = db.query(ProjectModel).order_by(sort_column.asc())
    else:
        projects_query = db.query(ProjectModel).order_by(sort_column.desc())

    # Apply filtering
    if active is not None:
        projects_query = projects_query.filter(ProjectModel.active == active)

    # Apply pagination
    projects = projects_query.offset(offset).limit(size).all()

    return projects

@router.get("/{project_id}", response_model=ProjectResponse)
def read_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(project_id: int, project: ProjectUpdate, db: Session = Depends(get_db)):
    db_project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    
    for key, value in project.dict(exclude_unset=True).items():
        setattr(db_project, key, value)
    
    db_project.updated_at = date.today()
    db.commit()
    db.refresh(db_project)
    return db_project

@router.delete("/{project_id}", response_model=ProjectResponse)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    db_project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    
    db.delete(db_project)
    db.commit()
    return db_project
