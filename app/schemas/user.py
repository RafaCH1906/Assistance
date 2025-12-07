from pydantic import BaseModel


class UserCreate(BaseModel):
    user: str
    password: str


class UserOut(BaseModel):
    id: int
    is_admin: bool

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

