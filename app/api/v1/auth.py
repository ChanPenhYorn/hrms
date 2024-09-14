from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.employee import Employee as EmployeeModel
from app.schemas.auth import UserLogin, Token
from app.schemas.employee import EmployeeCreate
from app.db.session import get_db
from app.utils.utils import hash_password, verify_password, create_access_token

router = APIRouter()

@router.post("/register", response_model=Token)
def register(user: EmployeeCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    db_user = db.query(EmployeeModel).filter(EmployeeModel.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    # Convert dob string to date object
    try:
        dob = datetime.strptime(user.dob, "%d-%m-%Y").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format for dob. Expected format is dd-MM-yyyy.")
    
    # Hash the password
    hashed_password = hash_password(user.password)
    
    # Create a new user
    new_user = EmployeeModel(
        email=user.email,
        password=hashed_password,
        firstname=user.firstname,
        lastname=user.lastname,
        gender=user.gender,
        dob=dob,  # Ensure dob is a date object
        department_id=user.department_id,
        project_id=user.project_id,
        position_id=user.position_id,
        photo=user.photo
    )
    
    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred while creating the user: {str(e)}")
    
    # Generate and return the token
    access_token = create_access_token({"email": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    # Verify user credentials
    db_user = db.query(EmployeeModel).filter(EmployeeModel.email == user.email).first()
    if db_user is None or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    # Generate and return the token
    access_token = create_access_token({"email": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}
