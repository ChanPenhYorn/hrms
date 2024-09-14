from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.employee import Employee as EmployeeModel
from app.schemas.employee import EmployeeResponse, EmployeeCreate, EmployeeUpdate
from sqlalchemy.exc import SQLAlchemyError
from passlib.context import CryptContext  # For hashing passwords

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/", response_model=EmployeeResponse)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    # Check if employee already exists
    db_employee = db.query(EmployeeModel).filter(
        EmployeeModel.firstname == employee.firstname,
        EmployeeModel.lastname == employee.lastname
    ).first()
    
    if db_employee:
        raise HTTPException(status_code=400, detail="Employee already exists")
    
    # Hash the password before storing it
    hashed_password = pwd_context.hash(employee.password)

    # Create a new employee
    new_employee = EmployeeModel(
        firstname=employee.firstname,
        lastname=employee.lastname,
        gender=employee.gender,
        dob=employee.dob,
        active=employee.active,
        photo=employee.photo,
        email=employee.email,
        password=hashed_password  # Assuming you have a password field in your model
    )
    
    db.add(new_employee)
    try:
        db.commit()
        db.refresh(new_employee)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while creating the employee")
    
    return new_employee

@router.get("/", response_model=List[EmployeeResponse])
def get_employees(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    # Retrieve employees with pagination
    employees = db.query(EmployeeModel).offset(skip).limit(limit).all()
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
        if key == "password" and value:
            # Hash the new password before updating
            value = pwd_context.hash(value)
        setattr(db_employee, key, value)
    
    try:
        db.commit()
        db.refresh(db_employee)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while updating the employee")
    
    return db_employee

@router.delete("/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    # Delete employee by ID
    db_employee = db.query(EmployeeModel).filter(EmployeeModel.id == employee_id).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    db.delete(db_employee)
    try:
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while deleting the employee")
    
    return {"detail": "Employee deleted"}
