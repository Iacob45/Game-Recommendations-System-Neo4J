from pydantic import BaseModel, Field


class RateGameRequest(BaseModel):
    score: int = Field(ge=1, le=10)
