from datetime import datetime, date, time, timedelta
from decimal import Decimal
from zoneinfo import ZoneInfo

from app.models.attendance import Attendance
from app.models.employee import Employee

LIMA = ZoneInfo("America/Lima")


def now_lima():
    return datetime.now(LIMA)


def calculate_hours_and_pay(hour_in: time, hour_out: time, pay_per_hour) -> tuple[float, Decimal]:
    #Convertimos las horas a datetime para poder restarlas
    today = date.today()
    dt_in = datetime.combine(today, hour_in).replace(tzinfo=LIMA)
    dt_out = datetime.combine(today, hour_out).replace(tzinfo=LIMA)
    if dt_out < dt_in:
        # Ajustar para el día siguiente si hour_out es antes que hour_in
        dt_out += timedelta(days=1)
    delta = dt_out - dt_in
    total_hours = Decimal(delta.total_seconds()) / Decimal(3600)
    # Calcular el pago total
    pay_dec = Decimal(str(pay_per_hour))
    total_pay = total_hours * pay_dec
    return float(total_hours), total_pay


def create_attendance_entry(db, employee: Employee):
    # Crear una nueva entrada de asistencia
    now = now_lima()
    attendance = Attendance(
        employee_id=employee.id,
        date=now.date(),
        hour_int=now.time(),
    )
    db.add(attendance)
    db.commit()
    db.refresh(attendance)
    return attendance


def close_attendance(db, attendance: Attendance, hour_out_time: time, overridden_by=None, reason: str | None = None, is_manual=False):
    # Ensure attendance.employee is loaded or fetch it
    if not getattr(attendance, 'employee', None):
        # lazy load employee
        from app.models.employee import Employee as EmployeeModel
        employee = db.query(EmployeeModel).filter(EmployeeModel.id == attendance.employee_id).first()
        attendance.employee = employee
    total_hours, total_pay = calculate_hours_and_pay(attendance.hour_int, hour_out_time, attendance.employee.pay_per_hour)
    attendance.hour_out = hour_out_time
    attendance.total_hours = total_hours
    attendance.total_pay = total_pay
    if is_manual:
        attendance.is_manual_override = True
        attendance.override_reason = reason
        attendance.overridden_by = overridden_by
        attendance.override_at = now_lima()
    db.add(attendance)
    db.commit()
    db.refresh(attendance)
    return attendance
