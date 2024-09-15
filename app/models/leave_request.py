from sqlalchemy import Column, Integer, String, Date, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class LeaveRequest(Base):
    __tablename__ = "leave_requests"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, nullable=False)
    reason = Column(String(255), nullable=False)
    leave_type_id = Column(Integer, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    status = Column(String(255), nullable=False)
    requested_on = Column(Date, nullable=False, default=func.current_date())
    approved_id = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=func.now())
    created_by = Column(String(255), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    updated_by = Column(String(255), nullable=True)
