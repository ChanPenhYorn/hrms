from sqlalchemy import Column, Integer, String, Boolean, Date
from sqlalchemy.sql import func
from app.db.base import Base
from sqlalchemy.orm import relationship

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    description = Column(String(255), nullable=True)
    active = Column(Boolean)  # Use Boolean for tinyint(1)
    created_by = Column(String(255))
    created_at = Column(Date, default=func.now())
    updated_by = Column(String(255), nullable=True)
    updated_at = Column(Date, default=func.now(), onupdate=func.now())

    # Define the relationship
    employees = relationship('Employee', back_populates='project')
