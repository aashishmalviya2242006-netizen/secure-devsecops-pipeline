from fastapi import Depends
from app.core import get_current_user
from fastapi import APIRouter, HTTPException, status

from app.schemas import (
        RegisterRequest,
        LoginRequest,
        TokenResponse,
)
from app.services.auth_service import auth_service

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.get("/")
def auth_home():
    return {
        "message": "Authentication service is working"
    }


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED
)
def register(user: RegisterRequest):

    registered_user = auth_service.register(user)

    if registered_user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    return registered_user

@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(user: LoginRequest):

    token = auth_service.authenticate_user(
        user.email,
        user.password,
    )

    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    return token

@router.get(
    "/me",
)
def get_me(current_user=Depends(get_current_user)):
    return current_user
