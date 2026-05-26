from pydantic import BaseModel, Field


class GameCreate(BaseModel):
    id: str
    title: str
    release_year: int | None = None
    genres: list[str] = Field(default_factory=list)
    platforms: list[str] = Field(default_factory=list)
    developer: str | None = None
    publisher: str | None = None


class GameResponse(BaseModel):
    id: str
    title: str
    release_year: int | None
    genres: list[str]
    platforms: list[str]
    developer: str | None
    publisher: str | None


class RateGameRequest(BaseModel):
    score: int = Field(ge=1, le=10)
