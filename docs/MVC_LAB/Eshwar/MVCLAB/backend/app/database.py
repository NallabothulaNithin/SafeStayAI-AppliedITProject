import os
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, session, sessionmaker

DATABASE_URL = os.environ["DATABASE_URL"]


engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """ALL ORM Models inherit from this."""

def get_db():
    """Dependency to get DB session."""
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()    