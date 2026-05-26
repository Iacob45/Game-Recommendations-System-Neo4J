from fastapi import APIRouter, HTTPException, status

from app.models.game import GameCreate, GameResponse
from app.services.game_service import GameService

router = APIRouter(prefix="/games", tags=["Games"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=GameResponse)
def create_game(body: GameCreate):
    return GameService.create_game(body)


@router.get("", response_model=list[GameResponse])
def get_games():
    return GameService.get_games()


@router.get("/{game_id}", response_model=GameResponse)
def get_game_by_id(game_id: str):
    game = GameService.get_game_by_id(game_id)

    if not game:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Game not found")

    return game
