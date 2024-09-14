from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.employee import Employee
from app.schemas.auth import UserCreate, UserLogin, Token
from app.db.session import get_db
from app.utils.utils import hash_password, verify_password, create_access_token

router = APIRouter()

@router.post("/register", response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    db_user = db.query(Employee).filter(Employee.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    # Create a new user
    hashed_password = hash_password(user.password)
    db_user = Employee(
        email=user.email,
        password=hashed_password,
        firstname=user.firstname,
        lastname=user.lastname,
        gender=user.gender,
        dob=user.dob,
        department_id=user.department_id,
        project_id=user.project_id,
        position_id=user.position_id,
        photo=user.photo
    )
    db.add(db_user)
    db.commit()
    return {"access_token": create_access_token(email=user.email), "token_type": "bearer"}

@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    # Verify user credentials
    db_user = db.query(Employee).filter(Employee.email == user.email).first()
    if db_user is None or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    # Generate token
    return {"access_token": create_access_token(email=user.email), "token_type": "bearer"}
