from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings


# Configuracion de la base de datos usando SQLAlchemy
engine = create_engine(settings.DB_URL, echo=True)

# Crear una clase SessionLocal para manejar las sesiones de la base de datos
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear una clase Base para definir los modelos de la base de datos
Base = declarative_base()

# Dependencia para obtener una sesion de la base de datos
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()