from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.models.department import Department as DepartmentModel
from app.schemas.department import DepartmentCreate, DepartmentResponse, DepartmentUpdate
from app.db.session import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/", response_model=DepartmentResponse)
def create_department(department: DepartmentCreate, db: Session = Depends(get_db)):
    db_department = DepartmentModel(
        name=department.name,
        active=department.active,
        created_by=department.created_by,
        updated_by=department.updated_by,
        description=department.description,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department

@router.get("/", response_model=List[DepartmentResponse])
def read_departments(db: Session = Depends(get_db)):
    return db.query(DepartmentModel).all()

@router.get("/{department_id}", response_model=DepartmentResponse)
def read_department(department_id: int, db: Session = Depends(get_db)):
    department = db.query(DepartmentModel).filter(DepartmentModel.id == department_id).first()
    if department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return department

@router.put("/{department_id}", response_model=DepartmentResponse)
def update_department(department_id: int, department: DepartmentUpdate, db: Session = Depends(get_db)):
    db_department = db.query(DepartmentModel).filter(DepartmentModel.id == department_id).first()
    if db_department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    
    for key, value in department.dict(exclude_unset=True).items():
        setattr(db_department, key, value)
    
    db_department.updated_at = datetime.now()
    db.commit()
    db.refresh(db_department)
    return db_department

@router.delete("/{department_id}", response_model=DepartmentResponse)
def delete_department(department_id: int, db: Session = Depends(get_db)):
    db_department = db.query(DepartmentModel).filter(DepartmentModel.id == department_id).first()
    if db_department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    
    db.delete(db_department)
    db.commit()
    return db_department
