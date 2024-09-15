from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.attendance import Attendance as AttendanceModel
from app.schemas.attendance import AttendanceCreate, AttendanceUpdate, AttendanceResponse
from app.db.session import get_db
from datetime import datetime

router = APIRouter()

# Create Attendance
@router.post("/", response_model=AttendanceResponse)
def create_attendance(attendance: AttendanceCreate, db: Session = Depends(get_db)):
    db_attendance = AttendanceModel(
        type=attendance.type,
        employee_id=attendance.employee_id,
        action_at=attendance.action_at,
        status=attendance.status,
        created_by=attendance.created_by,
        updated_by=attendance.updated_by,
        working_date=attendance.working_date,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    return db_attendance

# Read all Attendances (with pagination, filtering, and sorting)
@router.get("/", response_model=List[AttendanceResponse])
def read_attendances(
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
    sort_column = getattr(AttendanceModel, sort, None)
    if not sort_column:
        raise HTTPException(status_code=400, detail="Invalid sort field")

    query = db.query(AttendanceModel).order_by(getattr(sort_column, direction)())

    # Filter by status
    if status is not None:
        query = query.filter(AttendanceModel.status == status)

    # Filter by employee_id
    if employee_id is not None:
        query = query.filter(AttendanceModel.employee_id == employee_id)

    attendances = query.offset(offset).limit(size).all()

    return attendances

# Read Attendance by ID
@router.get("/{attendance_id}", response_model=AttendanceResponse)
def read_attendance(attendance_id: int, db: Session = Depends(get_db)):
    attendance = db.query(AttendanceModel).filter(AttendanceModel.id == attendance_id).first()
    if attendance is None:
        raise HTTPException(status_code=404, detail="Attendance not found")
    return attendance

# Update Attendance by ID
@router.put("/{attendance_id}", response_model=AttendanceResponse)
def update_attendance(attendance_id: int, attendance: AttendanceUpdate, db: Session = Depends(get_db)):
    db_attendance = db.query(AttendanceModel).filter(AttendanceModel.id == attendance_id).first()
    if db_attendance is None:
        raise HTTPException(status_code=404, detail="Attendance not found")

    for key, value in attendance.dict(exclude_unset=True).items():
        setattr(db_attendance, key, value)

    db_attendance.updated_at = datetime.now()
    db.commit()
    db.refresh(db_attendance)
    return db_attendance

# Delete Attendance by ID
@router.delete("/{attendance_id}", response_model=AttendanceResponse)
def delete_attendance(attendance_id: int, db: Session = Depends(get_db)):
    db_attendance = db.query(AttendanceModel).filter(AttendanceModel.id == attendance_id).first()
    if db_attendance is None:
        raise HTTPException(status_code=404, detail="Attendance not found")

    db.delete(db_attendance)
    db.commit()
    return db_attendance
