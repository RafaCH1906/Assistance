from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.employee import EmployeeCreate, EmployeeOut, EmployeeExitUpdate
from app.models.employee import Employee
from app.service.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/employee", tags=["employee"])


@router.post("/", response_model=EmployeeOut, status_code=status.HTTP_201_CREATED)
def create_employee(data: EmployeeCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Sólo jefes pueden crear empleados
    new_employee = Employee(
        name=data.name,
        lastname=data.lastname,
        pay_per_hour=data.pay_per_hour,
        owner_id=current_user.id,
    )
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee


@router.get("/", response_model=List[EmployeeOut])
def get_list_employee(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    employees = db.query(Employee).filter(Employee.owner_id == current_user.id).all()
    return employees


@router.put("/{employee_id}/exit_time", response_model=EmployeeOut)
def update_exit_time(employee_id: int, payload: EmployeeExitUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    employee = db.query(Employee).filter(Employee.id == employee_id, Employee.owner_id == current_user.id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    employee.exit_time = payload.exit_time
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee
