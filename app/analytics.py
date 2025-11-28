from .models import Movie, User, Stream, Rating
from .database import get_session
from sqlmodel import Session, select
from sqlalchemy import func


def top_rated_by_genre(session: Session, genre: str, limit: int = 5):
    movies = session.exec(
        select(Movie).where(Movie.genre == genre).order_by(Movie.average_rating.desc())
    ).all()
    return movies[:limit]

def most_watched_per_month(session: Session):
    # Use SQLite-compatible month extraction via strftime and return dicts
    month_label = func.strftime('%Y-%m', Stream.watch_date)
    rows = session.exec(
        select(
            Stream.movie_id,
            month_label.label("month"),
            func.count(Stream.id).label("watch_count")
        ).group_by(Stream.movie_id, month_label).order_by(func.count(Stream.id).desc())
    ).all()

    # Convert result rows to list of dicts for JSON serialization
    result = []
    for row in rows:
        # row may be a Row | tuple-like: unpack by index or attribute
        try:
            movie_id, month, watch_count = row
        except Exception:
            movie_id = getattr(row, 'movie_id', None)
            month = getattr(row, 'month', None)
            watch_count = getattr(row, 'watch_count', None)
        result.append({
            'movie_id': movie_id,
            'month': month,
            'watch_count': int(watch_count) if watch_count is not None else 0
        })
    return result

def total_watch_time_per_user(session: Session, user_id: int):
    total = session.exec(
        select(func.sum(Stream.watched_duration)).where(Stream.user_id == user_id)
    ).one_or_none()
    if total is None:
        return 0
    # total may be a tuple or a single value depending on SQLModel version
    if isinstance(total, (tuple, list)):
        value = total[0]
    else:
        value = total
    return value or 0
