from sqlalchemy import Column, Integer, String, Float, ForeignKey, Time
from sqlalchemy.orm import relationship

from app.database import Base


class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    lastname = Column(String, index=True)
    pay_per_hour = Column(Float, index=True)

    # relación con el jefe (owner)
    owner_id = Column(Integer, ForeignKey("users.id"), index=True)
    owner = relationship("User", back_populates="employees")

    # Hora de salida configurada por el jefe (solo hora)
    exit_time = Column(Time, nullable=True)

    # relación con asistencias
    attendances = relationship("Attendance", back_populates="employee")
