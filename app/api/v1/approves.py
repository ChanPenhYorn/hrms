from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.approve import Approve as ApproveModel
from app.schemas.approve import ApproveCreate, ApproveResponse, ApproveUpdate
from app.db.session import get_db

router = APIRouter()

# Create Approve
@router.post("/", response_model=ApproveResponse)
def create_approve(approve: ApproveCreate, db: Session = Depends(get_db)):
    db_approve = ApproveModel(
        is_approved=approve.is_approved,
        approved_by=approve.approved_by,
        approved_at=approve.approved_at or datetime.now(),
        description=approve.description,
        created_by=approve.created_by,
        updated_by=approve.updated_by,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(db_approve)
    db.commit()
    db.refresh(db_approve)
    return db_approve

# Read Approves (with pagination, filtering, and sorting)
@router.get("/", response_model=List[ApproveResponse])
def read_approves(
    page: int = Query(1, gt=0),
    size: int = Query(10, gt=0),
    sort: str = Query("created_at"),
    direction: str = Query("asc"),
    is_approved: Optional[bool] = None,  # Optional filter parameter
    db: Session = Depends(get_db)
):
    # Validate the sort direction
    if direction not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Sort direction must be 'asc' or 'desc'")

    # Calculate offset for pagination
    offset = (page - 1) * size

    # Create the sorting order
    sort_column = getattr(ApproveModel, sort, None)
    if not sort_column:
        raise HTTPException(status_code=400, detail="Invalid sort field")

    if direction == "asc":
        approves_query = db.query(ApproveModel).order_by(sort_column.asc())
    else:
        approves_query = db.query(ApproveModel).order_by(sort_column.desc())

    # Apply filtering
    if is_approved is not None:
        approves_query = approves_query.filter(ApproveModel.is_approved == is_approved)

    # Apply pagination
    approves = approves_query.offset(offset).limit(size).all()

    return approves

# Read Approve by ID
@router.get("/{approve_id}", response_model=ApproveResponse)
def read_approve(approve_id: int, db: Session = Depends(get_db)):
    approve = db.query(ApproveModel).filter(ApproveModel.id == approve_id).first()
    if approve is None:
        raise HTTPException(status_code=404, detail="Approve not found")
    return approve

# Update Approve by ID
@router.put("/{approve_id}", response_model=ApproveResponse)
def update_approve(approve_id: int, approve: ApproveUpdate, db: Session = Depends(get_db)):
    db_approve = db.query(ApproveModel).filter(ApproveModel.id == approve_id).first()
    if db_approve is None:
        raise HTTPException(status_code=404, detail="Approve not found")

    for key, value in approve.dict(exclude_unset=True).items():
        setattr(db_approve, key, value)

    db_approve.updated_at = datetime.now()
    db.commit()
    db.refresh(db_approve)
    return db_approve

# Delete Approve by ID
@router.delete("/{approve_id}", response_model=ApproveResponse)
def delete_approve(approve_id: int, db: Session = Depends(get_db)):
    db_approve = db.query(ApproveModel).filter(ApproveModel.id == approve_id).first()
    if db_approve is None:
        raise HTTPException(status_code=404, detail="Approve not found")

    db.delete(db_approve)
    db.commit()
    return db_approve
