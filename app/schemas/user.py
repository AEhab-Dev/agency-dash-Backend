from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: str
    full_name: str
    plan: str
    created_at: datetime

    model_config = {"from_attributes": True}


class UserWithTokens(BaseModel):
    user: UserOut
    access_token: str
    refresh_token: str
    token_type: str = "bearer"