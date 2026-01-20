import os

os.environ["DATABASE_URL"] = "sqlite:///./test.db"

import pytest  # noqa: E402
from sqlalchemy import create_engine  # noqa: E402
from sqlalchemy.orm import sessionmaker  # noqa: E402

# Импорт моделей для регистрации метаданных SQLAlchemy
import backend.models.follow  # noqa: F401, E402
import backend.models.like  # noqa: F401, E402
import backend.models.media  # noqa: F401, E402
import backend.models.tweet  # noqa: F401, E402
import backend.models.user  # noqa: F401, E402
from backend.core import db as db_module  # noqa: E402
from backend.core.db import Base  # noqa: E402
from backend.main import app  # noqa: E402
from backend.models.user import User  # noqa: E402

TEST_DB_URL = "sqlite:///./test.db"


@pytest.fixture(scope="function")
def engine():
    engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    return engine


@pytest.fixture(scope="function")
def db_session(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def test_user(db_session):
    user = User(name="Test User", api_key="test")
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def second_user(db_session):
    user = User(name="Second User", api_key="test2")
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def client(db_session, test_user):
    db_module.SessionLocal = lambda: db_session
    with app.test_client() as client:
        yield client


@pytest.fixture
def auth_headers():
    return {"api-key": "test"}
