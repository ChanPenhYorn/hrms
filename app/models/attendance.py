from sqlalchemy import Column, Integer, String, DateTime, Date
from sqlalchemy.sql import func
from app.db.base import Base

class Attendance(Base):
    __tablename__ = "attendances"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(255), nullable=False)
    employee_id = Column(Integer, nullable=False)
    action_at = Column(DateTime, nullable=False)
    status = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.now())
    created_by = Column(String(255), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    updated_by = Column(String(255), nullable=True)
    working_date = Column(Date, nullable=False)
