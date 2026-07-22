from fastapi import APIRouter, HTTPException, status

from app.schemas import RegisterRequest, LoginRequest
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

@router.post("/login")
def login(user: LoginRequest):

    authenticated_user = auth_service.authenticate_user(
        user.email,
        user.password
    )

    if authenticated_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    return authenticated_user
