from pydantic import BaseModel
from typing import Optional
from datetime import date, time

# Creamos los esquemas para la asistencia
class AttendanceOut(BaseModel):
    id: int
    employee_id: int
    date: date
    hour_int: Optional[time]
    hour_out: Optional[time]
    total_hours: Optional[float]
    total_pay: Optional[float]
    is_manual_override: Optional[bool]
    override_reason: Optional[str]

    class Config:
        orm_mode = True

# Creamos los esquemas para las operaciones de asistencia
class OverrideIn(BaseModel):
    new_exit_time: time
    reason: str


class MarkExitIn(BaseModel):
    # Optional: allow passing a specific exit time; if omitted, use now
    exit_time: Optional[time] = None
