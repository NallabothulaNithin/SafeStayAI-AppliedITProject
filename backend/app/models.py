from datetime import datetime

from sqlalchemy import ForeignKey, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))

    tasks: Mapped[list["Task"]] = relationship(back_populates="owner")

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    owner: Mapped["User"] = relationship(back_populates="tasks")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())