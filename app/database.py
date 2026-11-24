
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get database URL
DATABASE_URL = os.getenv("DATABASE_URL")

# Validate database URL
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is missing from .env")

# Create database engine
engine = create_engine(
    DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)
)

# Create database sessions
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for database models
Base = declarative_base()

# Database dependency
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
