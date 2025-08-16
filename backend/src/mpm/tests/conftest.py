import tempfile
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# point to your main app
from mpm.main import app
from mpm.database import Base, get_db

# Use a temporary SQLite file for tests
TEST_DB = tempfile.NamedTemporaryFile(suffix=".sqlite", delete=False).name
SQLALCHEMY_DATABASE_URL = f"sqlite:///{TEST_DB}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# override the get_db dependency
def override_get_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c
