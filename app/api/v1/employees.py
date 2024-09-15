from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.employee import Employee as EmployeeModel
from app.schemas.employee import EmployeeResponse, EmployeeCreate, EmployeeUpdate

router = APIRouter()

@router.post("/", response_model=EmployeeResponse)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    # Check if employee already exists
    db_employee = db.query(EmployeeModel).filter(
        EmployeeModel.firstname == employee.firstname,
        EmployeeModel.lastname == employee.lastname
    ).first()
    
    if db_employee:
        raise HTTPException(status_code=400, detail="Employee already exists")
    
    # Create a new employee
    new_employee = EmployeeModel(
        firstname=employee.firstname,
        lastname=employee.lastname,
        gender=employee.gender,
        dob=employee.dob,
        active=employee.active,
        photo=employee.photo,
        email=employee.email
    )
    
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee

# @router.get("/", response_model=List[EmployeeResponse])
# def get_employees(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     # Retrieve employees with pagination
#     employees = db.query(EmployeeModel).offset(skip).limit(limit).all()
#     return employees

@router.get("/", response_model=List[EmployeeResponse])
def get_employees(
    page: int = Query(1, gt=0),
    size: int = Query(10, gt=0),
    sort: str = Query("firstname"),
    direction: str = Query("asc"),
    db: Session = Depends(get_db)
):
    # Validate the sort direction
    if direction not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Sort direction must be 'asc' or 'desc'")
    
    # Calculate offset for pagination
    offset = (page - 1) * size

    # Create the sorting order
    sort_column = getattr(EmployeeModel, sort, None)
    if not sort_column:
        raise HTTPException(status_code=400, detail="Invalid sort field")
    
    if direction == "asc":
        employees_query = db.query(EmployeeModel).order_by(sort_column.asc())
    else:
        employees_query = db.query(EmployeeModel).order_by(sort_column.desc())

    # Apply pagination
    employees = employees_query.offset(offset).limit(size).all()

    return employees

@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    # Retrieve employee by ID
    employee = db.query(EmployeeModel).filter(EmployeeModel.id == employee_id).first()
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@router.put("/{employee_id}", response_model=EmployeeResponse)
def update_employee(employee_id: int, employee: EmployeeUpdate, db: Session = Depends(get_db)):
    # Update employee by ID
    db_employee = db.query(EmployeeModel).filter(EmployeeModel.id == employee_id).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    for key, value in employee.dict(exclude_unset=True).items():
        setattr(db_employee, key, value)
    
    db.commit()
    db.refresh(db_employee)
    return db_employee

@router.delete("/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    # Delete employee by ID
    db_employee = db.query(EmployeeModel).filter(EmployeeModel.id == employee_id).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    db.delete(db_employee)
    db.commit()
    return {"detail": "Employee deleted"}
