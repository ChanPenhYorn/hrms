from sqlalchemy import Column, Date, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime
from app.models.department import Department
from app.models.project import Project
from app.models.position import Position

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String, index=True)
    lastname = Column(String, index=True)
    gender = Column(String)
    dob = Column(Date)  # Changed to Date type for storing dates
    active = Column(Boolean, default=True)
    # department_id = Column(Integer, ForeignKey(Department.id))
    # project_id = Column(Integer, ForeignKey(Project.id))
    # position_id = Column(Integer, ForeignKey(Position.id))
    photo = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)  # Add this field
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(String, nullable=True)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    updated_by = Column(String, nullable=True)

    # # Define relationships if necessary
    # department = relationship(Department)  # Assuming you have a Department model
    # project = relationship(Project)  # Assuming you have a Project model
    # position = relationship(Position)  # Assuming you have a Position model
