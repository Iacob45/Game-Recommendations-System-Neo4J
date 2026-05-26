from fastapi import APIRouter, HTTPException, status

from app.models.game import RateGameRequest
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


@router.post("/{user_id}/play/{game_id}")
def play_game(user_id: str, game_id: str):
    result = UserService.play_game(user_id, game_id)

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User or game not found")

    return {
        "message": "Game marked as played",
        **result
    }


@router.post("/{user_id}/like/{game_id}")
def like_game(user_id: str, game_id: str):
    result = UserService.like_game(user_id, game_id)

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User or game not found")

    return {
        "message": "Game marked as liked",
        **result
    }


@router.post("/{user_id}/rate/{game_id}")
def rate_game(user_id: str, game_id: str, body: RateGameRequest):
    result = UserService.rate_game(user_id, game_id, body.score)

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User or game not found")

    return {
        "message": "Game rated successfully",
        **result
    }
