from .models import Movie, User, Stream, Rating
from .database import get_session
from sqlmodel import Session, select
from sqlalchemy import func


# ----- Movie CRUD -----
def create_movie(session: Session, movie: Movie):
    session.add(movie)
    session.commit()
    session.refresh(movie)
    return movie

def get_movie(session: Session, movie_id: int):
    return session.get(Movie, movie_id)

def update_movie(session: Session, movie: Movie):
    session.add(movie)
    session.commit()
    session.refresh(movie)
    return movie

def delete_movie(session: Session, movie: Movie):
    session.delete(movie)
    session.commit()

# ----- User CRUD -----
def create_user(session: Session, user: User):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

# ----- Streams & Ratings -----
def record_stream(session: Session, stream: Stream):
    session.add(stream)
    session.commit()
    session.refresh(stream)
    return stream

def submit_rating(session: Session, rating: Rating):
    session.add(rating)
    session.commit()
    session.refresh(rating)

    # Update average rating (simulating trigger)
    avg_rating = session.exec(
        select(func.avg(Rating.rating)).where(Rating.movie_id == rating.movie_id)
    ).one()
    movie = session.get(Movie, rating.movie_id)
    if movie:
        movie.average_rating = avg_rating or 0
        session.add(movie)
        session.commit()
    
    session.refresh(rating)
    return rating
