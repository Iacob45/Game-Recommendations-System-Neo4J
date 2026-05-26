from fastapi import APIRouter

from app.services.performance_service import PerformanceService
from app.services.statistics_service import StatisticsService

router = APIRouter(tags=["Statistics"])


@router.get("/statistics")
def get_statistics():
    statistics = StatisticsService.get_statistics()
    games_by_genre = StatisticsService.get_games_by_genre()

    return {
        "general": statistics,
        "games_by_genre": games_by_genre
    }


@router.post("/indexes")
def create_indexes():
    return PerformanceService.create_indexes()


@router.get("/performance/test")
def run_performance_test():
    return PerformanceService.run_performance_test()
