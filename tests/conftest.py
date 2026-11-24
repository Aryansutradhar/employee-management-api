
import os
import pytest

from dotenv import load_dotenv
from sqlalchemy.engine import make_url
from sqlalchemy.orm import sessionmaker

# Load environment variables
load_dotenv()

# Get original database URL
database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise RuntimeError("DATABASE_URL is missing from .env")

# Switch to testing database BEFORE importing the application
test_url = make_url(database_url).set(
    database="employee_management_test"
)

os.environ["DATABASE_URL"] = test_url.render_as_string(
    hide_password=False
)



@pytest.fixture
def test_engine():
    from app.database import Base, engine

    Base.metadata.create_all(bind=engine)

    try:
        yield engine
    finally:
        Base.metadata.drop_all(bind=engine)




@pytest.fixture
def client(test_engine, monkeypatch):
    from fastapi.testclient import TestClient
    from app import main, database

    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine
    )

    # Patch all session factories to use the test database
    monkeypatch.setattr(main, "SessionLocal", TestingSessionLocal)
    monkeypatch.setattr(database, "SessionLocal", TestingSessionLocal)

    with TestClient(main.app) as test_client:
        yield test_client
