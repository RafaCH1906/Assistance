from sqlalchemy import Column, Integer, Float, ForeignKey, Date, Time, Boolean, String, DateTime, Numeric
from sqlalchemy.orm import relationship

from app.database import Base


class Attendance(Base):
    __tablename__ = "attendances"

    #Index sirve para mejorar la velocidad de las consultas
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    date = Column(Date)
    hour_int = Column(Time)
    hour_out = Column(Time)
    total_hours = Column(Float)
    total_pay = Column(Numeric(12, 4))

    # Campos para override
    is_manual_override = Column(Boolean, default=False)
    override_reason = Column(String, nullable=True)
    overridden_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    override_at = Column(DateTime, nullable=True)

    employee = relationship("Employee", back_populates="attendances")
