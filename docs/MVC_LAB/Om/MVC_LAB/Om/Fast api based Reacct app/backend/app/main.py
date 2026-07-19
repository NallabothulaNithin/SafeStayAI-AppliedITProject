from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from app.controllers.task_controller import router as task_router
from app.controllers.user_controller import router as user_router
from app.controllers.auth_controller import router as auth_router

from sqlalchemy import select
from app.database import SessionLocal
from app.models import User, Task
import os
from app.database import Base, engine
from app import models  # noqa: F401 - registers Task with Base.metadata
from app.auth.hashing import hash_password

app = FastAPI(title="MVC Task API")

#Base.metadata.create_all(bind=engine) 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(task_router, prefix="/tasks", tags=["tasks"])
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])

# 
def seed_users():
    """Insert two users if the table is empty."""
    with SessionLocal() as db:
        if db.scalars(select(User)).first() is not None:
            return
        db.add_all([User(name="Alice", password_hash=hash_password("pass123")), User(name="Bob", password_hash=hash_password("pass123"))
        ])
        db.commit()


seed_users()