from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import date, datetime
from zoneinfo import ZoneInfo

from app.database import Session
from app.models.employee import Employee
from app.models.attendance import Attendance
from app.service.attendance_service import now_lima, close_attendance

LIMA = ZoneInfo("America/Lima")

scheduler = BackgroundScheduler(timezone=LIMA)


def _job_check_and_close():
    db = Session()
    try:
        today = date.today()
        now = now_lima()
        # Buscar empleados con exit_time configurado
        employees = db.query(Employee).filter(Employee.exit_time != None).all()
        for emp in employees:
            # buscar attendance abierto del dia para este empleado
            attendance = (db.query(Attendance).filter(Attendance.employee_id == emp.id, Attendance.date == today,
                                                     Attendance.hour_out == None)
                          .order_by(Attendance.id.desc()).first())
            if not attendance:
                continue
            # construir datetime de salida para hoy
            dt_exit = datetime.combine(today, emp.exit_time).replace(tzinfo=LIMA)
            if now >= dt_exit:
                # aseguremos que attendance.employee esté disponible para el cálculo
                attendance.employee = emp
                close_attendance(db, attendance, emp.exit_time, overridden_by=None, reason=None, is_manual=False)
    finally:
        db.close()


def start_scheduler():
    #cada 1 minuto
    scheduler.add_job(_job_check_and_close, IntervalTrigger(minutes=1))
    scheduler.start()


def shutdown_scheduler():
    scheduler.shutdown(wait=False)

