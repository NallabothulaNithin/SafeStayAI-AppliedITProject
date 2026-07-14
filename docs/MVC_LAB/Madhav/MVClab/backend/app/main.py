from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controllers.task_controllers import router as task_router
from sqlalchemy import create_engine, text
from app.controllers.user_controller import router as user_router
from sqlalchemy import select
from app.database import SessionLocal
from app.models import Task, User
from app.auth.hashing import hash_password
from app.controllers.auth_controller import router as auth_router

import os

from app.database import Base, engine
from app import models
# from main import app

app = FastAPI(title="MVC Task API")

Base.metadata.create_all(bind=engine)

app.include_router(auth_router, prefix="/auth", tags=["auth"])

def seed_users():
    with SessionLocal() as db:
        if db.scalars(select(User)).first() is not None:
            return
        db.add_all([User(name="Ronaldo", password_hash=hash_password("password123")), User(name="Madhav", password_hash=hash_password("password123"))])
        db.commit()
 
seed_users()

# @app.get("/db-ping")
# def ping_db():
#     engine = create_engine(os.environ["DATABASE_URL"])
#     with engine.connect() as conn:
#         return {"postgres": conn.execute(text("SELECT version()")).scalar()}


#View runs on a different origin, so CORS is required

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(task_router, prefix="/tasks", tags=["tasks"])
app.include_router(user_router, prefix="/users", tags=["users"])