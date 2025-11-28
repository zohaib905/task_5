from pydantic import BaseModel

class MovieCreate(BaseModel):
    title: str
    genre: str
    release_year: int
    duration_minutes: int

class UserCreate(BaseModel):
    name: str
    email: str
    subscription_type: str

class StreamCreate(BaseModel):
    user_id: int
    movie_id: int
    watched_duration: int

class RatingCreate(BaseModel):
    user_id: int
    movie_id: int
    rating: int
