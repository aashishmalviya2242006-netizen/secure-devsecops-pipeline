from fastapi import APIRouter, HTTPException, status

from app.schemas.user import User, UserCreate, UserUpdate
from app.services import user_service

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/", response_model=list[User])
def get_users():
    return user_service.get_all_users()


@router.get("/{user_id}", response_model=User)
def get_user(user_id: int):
    user = user_service.get_user(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


@router.post(
    "/",
    response_model=User,
    status_code=status.HTTP_201_CREATED
)
def create_user(user: UserCreate):
    return user_service.create_user(user)


@router.put("/{user_id}", response_model=User)
def update_user(user_id: int, user: UserUpdate):
    updated_user = user_service.update_user(user_id, user)

    if updated_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return updated_user


@router.delete("/{user_id}")
def delete_user(user_id: int):
    deleted = user_service.delete_user(user_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return {
        "message": "User deleted successfully"
    }
