import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Adjust these imports if your app folder structure uses a different naming convention
from app.main import app
from app.database import Base, get_db
from app.controllers.auth_controller import get_current_user
from app.models import User

@pytest.fixture
def db_session():
    """Provides a fresh in-memory SQLite database instance for EACH test."""
    # StaticPool keeps the single connection alive so everything sees the same DB state
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    
    # Create the database schema tables
    Base.metadata.create_all(bind=engine)
    
    TestSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    db = TestSession()
    try:
        yield db
    finally:
        db.close()
        engine.dispose()

def _seed_user(db, name: str) -> User:
    """Helper function to insert a dummy user into the test database."""
    u = User()
    u.name = name
    u.password_hash = "dummy_hash"  # Change this to match your model's field name if needed
    
    db.add(u)
    db.commit()
    db.refresh(u)
    return u

@pytest.fixture
def alice(db_session):
    """Fixture to automatically seed a user named Alice."""
    return _seed_user(db_session, "Alice")

@pytest.fixture
def bob(db_session):
    """Fixture to automatically seed a user named Bob."""
    return _seed_user(db_session, "Bob")

@pytest.fixture
def client(db_session, alice):
    """Provides a TestClient logged in as Alice by overriding get_db and get_current_user."""
    # Dependency overrides route controller traffic to the test DB and test authentication
    app.dependency_overrides[get_db] = lambda: db_session
    app.dependency_overrides[get_current_user] = lambda: alice
    
    yield TestClient(app)
    
    # Clean up overrides after the test completes so subsequent tests get a fresh slate
    app.dependency_overrides.clear()