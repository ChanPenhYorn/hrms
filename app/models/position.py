from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.db.base import Base
from sqlalchemy.orm import relationship

class Position(Base):
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True, index=True)
    position = Column(String(255), index=True)
    active = Column(Boolean)  # Use Boolean for tinyint(1)
    description = Column(String(255), nullable=True)
    created_by = Column(Integer)  # Assuming created_by is an integer
    created_at = Column(DateTime, default=func.now())
    updated_by = Column(Integer, nullable=True)  # Assuming updated_by is an integer
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Define the relationship
    employees = relationship('Employee', back_populates='position')
