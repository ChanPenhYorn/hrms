from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.project import Project as ProjectModel
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate
from app.db.session import get_db
from sqlalchemy.orm import Session

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
def read_projects(db: Session = Depends(get_db)):
    return db.query(ProjectModel).all()

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
