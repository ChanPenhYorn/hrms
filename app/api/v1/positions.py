from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.position import Position as PositionModel
from app.schemas.position import PositionCreate, PositionResponse, PositionUpdate
from app.db.session import get_db
from sqlalchemy.orm import Session

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
def read_positions(db: Session = Depends(get_db)):
    return db.query(PositionModel).all()

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
