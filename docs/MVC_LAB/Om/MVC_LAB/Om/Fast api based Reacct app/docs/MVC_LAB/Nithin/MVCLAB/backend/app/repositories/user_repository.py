from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import User

class UserRepository:
    def __init__(self, db: Session):
        self._db = db

    def all(self) -> list[User]:
        return list(self._db.scalars(select(User)))
    
    def find(self, user_id: int) -> User:
        return self._db.get(User, user_id)