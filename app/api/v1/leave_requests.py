from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.leave_request import LeaveRequest as LeaveRequestModel
from app.schemas.leave_request import LeaveRequestCreate, LeaveRequestUpdate, LeaveRequestResponse
from app.db.session import get_db
from datetime import datetime

router = APIRouter()

# Create Leave Request
@router.post("/", response_model=LeaveRequestResponse)
def create_leave_request(leave_request: LeaveRequestCreate, db: Session = Depends(get_db)):
    db_leave_request = LeaveRequestModel(
        employee_id=leave_request.employee_id,
        reason=leave_request.reason,
        leave_type_id=leave_request.leave_type_id,
        start_date=leave_request.start_date,
        end_date=leave_request.end_date,
        status=leave_request.status,
        requested_on=leave_request.requested_on if leave_request.requested_on else datetime.now().date(),
        approved_id=leave_request.approved_id,
        created_by=leave_request.created_by,
        updated_by=leave_request.updated_by,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(db_leave_request)
    db.commit()
    db.refresh(db_leave_request)
    return db_leave_request

# Read all Leave Requests (with pagination, filtering, and sorting)
@router.get("/", response_model=List[LeaveRequestResponse])
def read_leave_requests(
    page: int = Query(1, gt=0),
    size: int = Query(10, gt=0),
    sort: str = Query("created_at"),
    direction: str = Query("asc"),
    status: Optional[str] = None,
    employee_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    # Validate sort direction
    if direction not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Sort direction must be 'asc' or 'desc'")

    # Calculate offset
    offset = (page - 1) * size

    # Sorting order
    sort_column = getattr(LeaveRequestModel, sort, None)
    if not sort_column:
        raise HTTPException(status_code=400, detail="Invalid sort field")

    query = db.query(LeaveRequestModel).order_by(getattr(sort_column, direction)())

    # Filter by status
    if status is not None:
        query = query.filter(LeaveRequestModel.status == status)

    # Filter by employee_id
    if employee_id is not None:
        query = query.filter(LeaveRequestModel.employee_id == employee_id)

    leave_requests = query.offset(offset).limit(size).all()

    return leave_requests

# Read Leave Request by ID
@router.get("/{leave_request_id}", response_model=LeaveRequestResponse)
def read_leave_request(leave_request_id: int, db: Session = Depends(get_db)):
    leave_request = db.query(LeaveRequestModel).filter(LeaveRequestModel.id == leave_request_id).first()
    if leave_request is None:
        raise HTTPException(status_code=404, detail="Leave request not found")
    return leave_request

# Update Leave Request by ID
@router.put("/{leave_request_id}", response_model=LeaveRequestResponse)
def update_leave_request(leave_request_id: int, leave_request: LeaveRequestUpdate, db: Session = Depends(get_db)):
    db_leave_request = db.query(LeaveRequestModel).filter(LeaveRequestModel.id == leave_request_id).first()
    if db_leave_request is None:
        raise HTTPException(status_code=404, detail="Leave request not found")

    for key, value in leave_request.dict(exclude_unset=True).items():
        setattr(db_leave_request, key, value)

    db_leave_request.updated_at = datetime.now()
    db.commit()
    db.refresh(db_leave_request)
    return db_leave_request

# Delete Leave Request by ID
@router.delete("/{leave_request_id}", response_model=LeaveRequestResponse)
def delete_leave_request(leave_request_id: int, db: Session = Depends(get_db)):
    db_leave_request = db.query(LeaveRequestModel).filter(LeaveRequestModel.id == leave_request_id).first()
    if db_leave_request is None:
        raise HTTPException(status_code=404, detail="Leave request not found")

    db.delete(db_leave_request)
    db.commit()
    return db_leave_request
