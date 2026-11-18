
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Load environment variables from .env
load_dotenv()

# Read database URL from .env
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./palm_mind.db"
)

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    """Provide a database session to API endpoints."""
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
