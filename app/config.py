import os
from dotenv import load_dotenv

#Lo que hacemos aca es cargar las variables de entorno desde un archivo .env
load_dotenv()


#Creamos una clase para manejar la configuracion de la aplicacion
class Settings:
    DB_URL: str = os.getenv("DB_URL")  # cadena de conexion a la base de datos

    # Secret key
    JWT_SECRET: str = os.getenv("JWT_SECRET")

    # Algoritmo para JWT
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM").upper()

    # Validar algoritmo
    _ALLOWED_ALGS = {"HS256", "RS256"}
    if JWT_ALGORITHM not in _ALLOWED_ALGS:
        JWT_ALGORITHM = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))


#Creamos una instancia de la clase Settings para usar en la aplicacion
settings = Settings()
