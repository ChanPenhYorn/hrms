from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from app.models.position import Position as PositionModel
from app.schemas.position import PositionCreate, PositionResponse, PositionUpdate
from app.db.session import get_db
from sqlalchemy.orm import Session
from typing import Optional

router = APIRouter()

@router.post("/", response_model=PositionResponse)
def create_position(position: PositionCreate, db: Session = Depends(get_db)):
    db_position = PositionModel(
        position=position.position,
        active=position.active,
        description=position.description,
        created_by=position.created_by,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(db_position)
    db.commit()
    db.refresh(db_position)
    return db_position


@router.get("/", response_model=List[PositionResponse])
def read_positions(
    page: int = Query(1, gt=0),
    size: int = Query(10, gt=0),
    sort: str = Query("position"),
    direction: str = Query("asc"),
    active: Optional[bool] = None,  # Optional filter parameter
    db: Session = Depends(get_db)
):
    # Validate the sort direction
    if direction not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Sort direction must be 'asc' or 'desc'")
    
    # Calculate offset for pagination
    offset = (page - 1) * size

    # Create the sorting order
    sort_column = getattr(PositionModel, sort, None)
    if not sort_column:
        raise HTTPException(status_code=400, detail="Invalid sort field")
    
    if direction == "asc":
        positions_query = db.query(PositionModel).order_by(sort_column.asc())
    else:
        positions_query = db.query(PositionModel).order_by(sort_column.desc())

    # Apply filtering
    if active is not None:
        positions_query = positions_query.filter(PositionModel.active == active)

    # Apply pagination
    positions = positions_query.offset(offset).limit(size).all()

    return positions

@router.get("/{position_id}", response_model=PositionResponse)
def read_position(position_id: int, db: Session = Depends(get_db)):
    position = db.query(PositionModel).filter(PositionModel.id == position_id).first()
    if position is None:
        raise HTTPException(status_code=404, detail="Position not found")
    return position

@router.put("/{position_id}", response_model=PositionResponse)
def update_position(position_id: int, position: PositionUpdate, db: Session = Depends(get_db)):
    db_position = db.query(PositionModel).filter(PositionModel.id == position_id).first()
    if db_position is None:
        raise HTTPException(status_code=404, detail="Position not found")
    
    for key, value in position.dict(exclude_unset=True).items():
        setattr(db_position, key, value)
    
    db_position.updated_at = datetime.now()
    db.commit()
    db.refresh(db_position)
    return db_position

@router.delete("/{position_id}", response_model=PositionResponse)
def delete_position(position_id: int, db: Session = Depends(get_db)):
    db_position = db.query(PositionModel).filter(PositionModel.id == position_id).first()
    if db_position is None:
        raise HTTPException(status_code=404, detail="Position not found")
    
    db.delete(db_position)
    db.commit()
    return db_position
