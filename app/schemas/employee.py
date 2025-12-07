from pydantic import BaseModel
from datetime import time

# Esquemas para la entidad Empleado
class EmployeeCreate(BaseModel):
    name: str
    lastname:str
    pay_per_hour: float

# Esquema para la respuesta al crear o leer un empleado
class EmployeeOut(BaseModel):
    id: int
    name: str
    lastname:str
    pay_per_hour: float

    #Esta clase interna permite que Pydantic trabaje con ORM como SQLAlchemy
    #ORM sirve para mapear objetos de Python a tablas de bases de datos relacionales
    class Config:
        orm_mode = True


class EmployeeExitUpdate(BaseModel):
    exit_time: time
