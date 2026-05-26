from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    id: str
    username: str
    age: int | None = None


class UserResponse(BaseModel):
    id: str
    username: str
    age: int | None
