from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import User


class UserRepository:
    def __init__(self, db: Session):
        self._db = db

    def all(self) -> list[User]:
        return list(self._db.scalars(select(User)))

    def find(self, user_id: int) -> User | None:
        return self._db.get(User, user_id)

    def find_by_name(self, name: str) -> User | None:
        return self._db.scalars(select(User).where(User.name == name)).first()

    def add(self, name: str, password_hash: str) -> User:
        user = User(name=name, password_hash=password_hash)
        self._db.add(user)
        self._db.commit()
        self._db.refresh(user)
        return user
