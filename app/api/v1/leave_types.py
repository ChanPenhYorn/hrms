from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.leave_type import LeaveType as LeaveTypeModel
from app.schemas.leave_type import LeaveTypeCreate, LeaveTypeUpdate, LeaveTypeResponse
from app.db.session import get_db
from datetime import datetime

router = APIRouter()

# Create LeaveType
@router.post("/", response_model=LeaveTypeResponse)
def create_leave_type(leave_type: LeaveTypeCreate, db: Session = Depends(get_db)):
    db_leave_type = LeaveTypeModel(
        type=leave_type.type,
        description=leave_type.description,
        created_by=leave_type.created_by,
        updated_by=leave_type.updated_by,
        active=leave_type.active,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(db_leave_type)
    db.commit()
    db.refresh(db_leave_type)
    return db_leave_type

# Read all LeaveTypes (with pagination, filtering, and sorting)
@router.get("/", response_model=List[LeaveTypeResponse])
def read_leave_types(
    page: int = Query(1, gt=0),
    size: int = Query(10, gt=0),
    sort: str = Query("created_at"),
    direction: str = Query("asc"),
    active: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    # Validate sort direction
    if direction not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Sort direction must be 'asc' or 'desc'")

    # Calculate offset
    offset = (page - 1) * size

    # Sorting order
    sort_column = getattr(LeaveTypeModel, sort, None)
    if not sort_column:
        raise HTTPException(status_code=400, detail="Invalid sort field")

    query = db.query(LeaveTypeModel).order_by(getattr(sort_column, direction)())
    
    # Filter by active
    if active is not None:
        query = query.filter(LeaveTypeModel.active == active)

    leave_types = query.offset(offset).limit(size).all()

    return leave_types

# Read LeaveType by ID
@router.get("/{leave_type_id}", response_model=LeaveTypeResponse)
def read_leave_type(leave_type_id: int, db: Session = Depends(get_db)):
    leave_type = db.query(LeaveTypeModel).filter(LeaveTypeModel.id == leave_type_id).first()
    if leave_type is None:
        raise HTTPException(status_code=404, detail="LeaveType not found")
    return leave_type

# Update LeaveType by ID
@router.put("/{leave_type_id}", response_model=LeaveTypeResponse)
def update_leave_type(leave_type_id: int, leave_type: LeaveTypeUpdate, db: Session = Depends(get_db)):
    db_leave_type = db.query(LeaveTypeModel).filter(LeaveTypeModel.id == leave_type_id).first()
    if db_leave_type is None:
        raise HTTPException(status_code=404, detail="LeaveType not found")

    for key, value in leave_type.dict(exclude_unset=True).items():
        setattr(db_leave_type, key, value)

    db_leave_type.updated_at = datetime.now()
    db.commit()
    db.refresh(db_leave_type)
    return db_leave_type

# Delete LeaveType by ID
@router.delete("/{leave_type_id}", response_model=LeaveTypeResponse)
def delete_leave_type(leave_type_id: int, db: Session = Depends(get_db)):
    db_leave_type = db.query(LeaveTypeModel).filter(LeaveTypeModel.id == leave_type_id).first()
    if db_leave_type is None:
        raise HTTPException(status_code=404, detail="LeaveType not found")

    db.delete(db_leave_type)
    db.commit()
    return db_leave_type
