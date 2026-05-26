from fastapi import APIRouter, HTTPException, status

from app.models.user import UserCreate, UserResponse
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(body: UserCreate):
    return UserService.create_user(body)


@router.get("", response_model=list[UserResponse])
def get_users():
    return UserService.get_users()


@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: str):
    user = UserService.get_user_by_id(user_id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user
