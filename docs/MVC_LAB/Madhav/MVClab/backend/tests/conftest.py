import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
 
from app.main import app
from app.database import Base, get_db
from app.controllers.auth_controller import get_current_user
from app.models import User
from app.auth.hashing import hash_password
 
@pytest.fixture
def db_session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        engine.dispose()
 
def _seed_user(db, name: str) -> User:
    u = User(name=name, password_hash=hash_password("password123"))
    db.add(u); db.commit(); db.refresh(u)
    return u
 
@pytest.fixture
def madhav(db_session):
    return _seed_user(db_session, "Madhav")
 
@pytest.fixture
def ronaldo(db_session):
    return _seed_user(db_session, "Ronaldo")
 
@pytest.fixture
def client(db_session, madhav):
    app.dependency_overrides[get_db] = lambda: db_session
    app.dependency_overrides[get_current_user] = lambda: madhav
    yield TestClient(app)
    app.dependency_overrides.clear()