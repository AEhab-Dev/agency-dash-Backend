from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.user import UserRegister, UserLogin, UserOut, UserWithTokens
from app.schemas.token import AccessToken, RefreshTokenRequest, LogoutRequest
from app.services.auth_service import register_user, login_user, refresh_access_token, logout_user

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=UserWithTokens)
def register(data: UserRegister, db: Session = Depends(get_db)):
    user, access_token, refresh_token = register_user(db, data)
    return UserWithTokens(
        user=UserOut.model_validate(user),
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post("/login", response_model=UserWithTokens)
def login(data: UserLogin, db: Session = Depends(get_db)):
    user, access_token, refresh_token = login_user(db, data.email, data.password)
    return UserWithTokens(
        user=UserOut.model_validate(user),
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post("/refresh", response_model=AccessToken)
def refresh(data: RefreshTokenRequest, db: Session = Depends(get_db)):
    access_token = refresh_access_token(db, data.refresh_token)
    return AccessToken(access_token=access_token)


@router.post("/logout")
def logout(data: LogoutRequest, db: Session = Depends(get_db)):
    logout_user(db, data.refresh_token)
    return {"detail": "Logged out successfully"}


@router.get("/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)):
    return UserOut.model_validate(current_user)