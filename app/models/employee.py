from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, ForeignKey
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
    department_id = Column(Integer, ForeignKey('departments.id'))  # Corrected table name
    project_id = Column(Integer, ForeignKey('projects.id'))  # Corrected table name
    position_id = Column(Integer, ForeignKey('positions.id'))  # Corrected table name?
    photo = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)  # Add this field
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(String, nullable=True)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    updated_by = Column(String, nullable=True)

    # Define relationships
    department = relationship('Department', back_populates='employees')
    project = relationship('Project', back_populates='employees')
    position = relationship('Position', back_populates='employees')
