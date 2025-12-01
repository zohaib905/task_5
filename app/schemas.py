from pydantic import BaseModel
from typing import Optional

class MovieCreate(BaseModel):
    title: str
    genre: str
    release_year: int
    duration_minutes: int
class MovieUpdate(BaseModel):
    title: str | None = None
    genre: str | None = None
    release_year: int | None = None
    duration_minutes: int | None = None
class MovieDelete(BaseModel):
    id: int



class UserCreate(BaseModel):
    name: str
    email: str
    subscription_type: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    subscription_type: Optional[str] = None

class StreamCreate(BaseModel):
    user_id: int
    movie_id: int
    watched_duration: int

class RatingCreate(BaseModel):
    user_id: int
    movie_id: int
    rating: int
