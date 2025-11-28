from sqlmodel import SQLModel, create_engine, Session
import os

# Use DATABASE_URL from env or default to a local SQLite file for convenience
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./moviedb.db")

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

# Initialize database tables
def init_db():
    # Ensure models are imported from the package so SQLModel metadata is populated
    import app.models  # noqa: F401
    SQLModel.metadata.create_all(engine)
