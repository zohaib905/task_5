# app/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import Session
from .database import init_db, get_session
from . import crud, analytics
from .models import Movie, User, Stream, Rating
from .schemas import MovieCreate, UserCreate, StreamCreate, RatingCreate


app = FastAPI(title="Movie Streaming Analytics API")

# Initialize DB
init_db()

# ----- Movies CRUD -----
@app.post("/movies/", status_code=status.HTTP_201_CREATED, response_model=Movie)
def create_movie(movie: MovieCreate, session: Session = Depends(get_session)):
    db_movie = Movie(**movie.model_dump())
    return crud.create_movie(session, db_movie)

@app.get("/movies/{movie_id}", response_model=Movie)
def get_movie(movie_id: int, session: Session = Depends(get_session)):
    movie = crud.get_movie(session, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

# ----- Users CRUD -----
@app.post("/users/", status_code=status.HTTP_201_CREATED, response_model=User)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    db_user = User(**user.model_dump())
    return crud.create_user(session, db_user)
@app.post("/streams/", status_code=status.HTTP_201_CREATED, response_model=Stream)
def record_stream(stream: StreamCreate, session: Session = Depends(get_session)):
    db_stream = Stream(**stream.model_dump())
    return crud.record_stream(session, db_stream)

@app.post("/ratings/", status_code=status.HTTP_201_CREATED, response_model=Rating)
def submit_rating(rating: RatingCreate, session: Session = Depends(get_session)):
    db_rating = Rating(**rating.model_dump())
    return crud.submit_rating(session, db_rating)

# ----- Analytics -----
@app.get("/analytics/top-rated/{genre}")
def top_rated(genre: str, session: Session = Depends(get_session)):
    return analytics.top_rated_by_genre(session, genre)

@app.get("/analytics/most-watched")
def most_watched(session: Session = Depends(get_session)):
    return analytics.most_watched_per_month(session)

@app.get("/analytics/user-watch-time/{user_id}")
def user_watch_time(user_id: int, session: Session = Depends(get_session)):
    return {"total_watch_time": analytics.total_watch_time_per_user(session, user_id)}
