from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controllers.task_controller  import router as task_router
from app.controllers.user_controller import router as user_router
from sqlalchemy import create_engine, text
from app.auth.hashing import hash_password

from sqlalchemy import select
from app.database import SessionLocal
from app.models import Task, User
import os

from app.database import Base, engine
from app import models
from app.controllers.auth_controller import router as auth_router

app = FastAPI(title="MVCLAB backend API")

Base.metadata.create_all(bind=engine)

app.include_router(
    auth_router,
    prefix="/api/auth",
    tags=["Authentication"]
)

# the view runs on a different origin, so CROS is required
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    task_router, 
    prefix="/api/tasks", 
    tags=["Tasks"]
    )

app.include_router(
    user_router,
    prefix="/api/users",
    tags=["Users"]
)

def seed_users():
    with SessionLocal() as db:
        if db.scalars(select(User)).first() is not None:
            return
        
        db.add_all([
            User(name="Doe", password_hash=hash_password("password123")), 
            User(name="Nithin", password_hash=hash_password("password123"))
        ])
        db.commit()

seed_users()        

# @app.get("/db-ping")
# def db_ping():
#     engine = create_engine(os.environ["DATABASE_URL"])
#     with engine.connect() as conn:
#         return {"postgres": conn.execute(text("SELECT version()")).scalar()}