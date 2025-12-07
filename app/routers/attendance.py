from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date

from app.database import get_db
from app.service.auth import get_current_user
from app.models.user import User
from app.models.employee import Employee
from app.models.attendance import Attendance
from app.service.attendance_service import create_attendance_entry, close_attendance, now_lima
from app.schemas.attendance import AttendanceOut, MarkExitIn, OverrideIn

router = APIRouter(prefix="/attendance", tags=["attendance"])


@router.post("/mark_entry/{employee_id}", response_model=AttendanceOut, status_code=status.HTTP_201_CREATED)
def mark_entry(employee_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    employee = db.query(Employee).filter(Employee.id == employee_id, Employee.owner_id == current_user.id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    attendance = create_attendance_entry(db, employee)
    return attendance


@router.post("/mark_exit/{employee_id}", response_model=AttendanceOut)
def mark_exit(employee_id: int, payload: MarkExitIn = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    employee = db.query(Employee).filter(Employee.id == employee_id, Employee.owner_id == current_user.id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    # buscar attendance abierto del dia
    today = date.today()
    attendance = db.query(Attendance).filter(Attendance.employee_id == employee.id, Attendance.date == today, Attendance.hour_out == None).order_by(Attendance.id.desc()).first()
    if not attendance:
        raise HTTPException(status_code=404, detail="No hay entrada abierta para hoy")
    # si payload y exit_time provisto, usarlo; sino usar ahora
    if payload and payload.exit_time:
        exit_t = payload.exit_time
    else:
        exit_t = now_lima().time()

    attendance = close_attendance(db, attendance, exit_t, overridden_by=current_user.id, reason=None, is_manual=True)
    return attendance


@router.patch("/{attendance_id}/override_exit", response_model=AttendanceOut)
def override_exit(attendance_id: int, payload: OverrideIn, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    attendance = db.query(Attendance).filter(Attendance.id == attendance_id).first()
    if not attendance:
        raise HTTPException(status_code=404, detail="Attendance no encontrado")
    employee = db.query(Employee).filter(Employee.id == attendance.employee_id).first()
    if not employee or employee.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="No autorizado")
    attendance = close_attendance(db, attendance, payload.new_exit_time, overridden_by=current_user.id, reason=payload.reason, is_manual=True)
    return attendance
