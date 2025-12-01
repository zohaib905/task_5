from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import Session
from .database import init_db, get_session
from . import crud, analytics
from .models import Movie, User, Stream, Rating
from .schemas import MovieCreate, MovieUpdate, UserCreate,UserUpdate, StreamCreate, RatingCreate
from sqlmodel import select

app = FastAPI(title="Movie Streaming Analytics API")

# Initialize DB

init_db()

# ----- Movies CRUD -----

@app.post("/movies/", status_code=status.HTTP_201_CREATED, response_model=Movie)

def create_movie(movie: MovieCreate, session: Session = Depends(get_session)):
      

      db_movie = Movie(**movie.model_dump())

      return crud.create_movie(session, db_movie)
@app.get("/movies/", response_model=list[Movie], status_code=200)
def get_all_movies(session: Session = Depends(get_session)):
    movies = session.exec(select(Movie)).all()
    return movies



@app.get("/movies/{movie_id}", response_model=Movie)

def get_movie(movie_id: int, session: Session = Depends(get_session)):
       
      
       movie = crud.get_movie(session, movie_id)



       if not movie:
           
           
              
           raise HTTPException(status_code=404, detail="Movie not found")
       return movie
@app.put("/movies/{movie_id}", response_model=Movie, status_code=status.HTTP_200_OK)
def update_movie(movie_id: int, movie_data: MovieUpdate, session: Session = Depends(get_session)):
    movie = crud.get_movie(session, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    for key, value in movie_data.model_dump(exclude_unset=True).items():
        setattr(movie, key, value)
    
    return crud.update_movie(session, movie)

# ----- Delete Movie -----
@app.delete("/movies/{movie_id}", status_code=status.HTTP_200_OK)
def delete_movie(movie_id: int, session: Session = Depends(get_session)):
    movie = crud.get_movie(session, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    return crud.delete_movie(session, movie)


@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user_data: UserUpdate, session: Session = Depends(get_session)):
    user = crud.get_user(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in user_data.model_dump(exclude_unset=True).items():
        setattr(user, key, value)

    return crud.update_user(session, user)

@app.delete("/users/{user_id}", status_code=200)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user = crud.get_user(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return crud.delete_user(session, user)


# ----- Users CRUD -----

@app.post("/users/", status_code=status.HTTP_201_CREATED, response_model=User)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
      
      
      db_user = User(**user.model_dump())

      return crud.create_user(session, db_user)

@app.get("/users/", response_model=list[User], status_code=200)
def get_all_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return users

@app.put("/users/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
def update_user(user_id: int, user_data: UserUpdate, session: Session = Depends(get_session)):
    user = crud.get_user(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update only provided fields
    for key, value in user_data.dict(exclude_unset=True).items():
        setattr(user, key, value)
    
    updated_user = crud.update_user(session, user)
    return updated_user

@app.delete("/users/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user = crud.get_user(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return crud.delete_user(session, user)
@app.delete("/users/", status_code=200)
def delete_all_users(session: Session = Depends(get_session)):
    return crud.delete_all_users(session)



# ----- Streams & Ratings -----

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
