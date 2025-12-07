from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, Token, UserOut
from app.config import settings
from app.service.auth import get_current_user_optional

router = APIRouter(prefix="/auth", tags=["auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


@router.post("/token", response_model=Token)
def login_for_access_token(form_data: UserCreate, db: Session = Depends(get_db)):
    # Reuse UserCreate (email + password) for login
    user = db.query(User).filter(User.email == form_data.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

#endpoint para crear un jefe (boss)
@router.post("/admin/create_boss", response_model=UserOut)
def create_boss(user_in: UserCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user_optional)):
    # Verificar si ya existe un admin en la base de datos
    admin_exists = db.query(User).filter(User.is_admin == True).first() is not None
    if admin_exists:
        if current_user is None or not current_user.is_admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admin can create boss accounts")
        user = User(email=user_in.email, hashed_password=get_password_hash(user_in.password), is_admin=False)
    else:
        # Si no existe un admin, permitir crear el primer jefe sin autenticacion
        user = User(email=user_in.email, hashed_password=get_password_hash(user_in.password), is_admin=True)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user
