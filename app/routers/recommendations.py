from fastapi import APIRouter, Query

from app.services.recommendation_service import RecommendationService

router = APIRouter(tags=["Recommendations"])


@router.get("/users/{user_id}/recommendations")
def get_recommendations_for_user(user_id: str, limit: int = Query(default=10, ge=1, le=50)):
    return RecommendationService.get_recommendations_for_user(user_id, limit)


@router.get("/users/{user_id}/similar-users")
def get_similar_users(user_id: str, limit: int = Query(default=10, ge=1, le=50)):
    return RecommendationService.get_similar_users(user_id, limit)


@router.get("/games/{game_id}/similar")
def get_similar_games(game_id: str, limit: int = Query(default=10, ge=1, le=50)):
    return RecommendationService.get_similar_games(game_id, limit)
