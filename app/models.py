from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime

class Movie(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    genre: str
    release_year: int
    duration_minutes: int
    average_rating: float = 0.0

    streams: List["Stream"] = Relationship(back_populates="movie")
    ratings: List["Rating"] = Relationship(back_populates="movie")


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    subscription_type: str

    streams: List["Stream"] = Relationship(back_populates="user")
    ratings: List["Rating"] = Relationship(back_populates="user")


class Stream(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    movie_id: int = Field(foreign_key="movie.id")
    watched_duration: int
    watch_date: datetime = Field(default_factory=datetime.utcnow)

    user: User = Relationship(back_populates="streams")
    movie: Movie = Relationship(back_populates="streams")


class Rating(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    movie_id: int = Field(foreign_key="movie.id")
    rating: int

    user: User = Relationship(back_populates="ratings")
    movie: Movie = Relationship(back_populates="ratings")
