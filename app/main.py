from fastapi import FastAPI
from .routers import employee, auth, attendance
from .database import Base, engine
from .tasks import start_scheduler, shutdown_scheduler

app = FastAPI(title="Sistema de Asistencia")

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)


@app.on_event("startup")
def on_startup():
    start_scheduler()


@app.on_event("shutdown")
def on_shutdown():
    shutdown_scheduler()

# Incluir routers
app.include_router(auth.router)
app.include_router(employee.router)
app.include_router(attendance.router)


@app.get("/")
def root():
    return {"message": "API lista"}
