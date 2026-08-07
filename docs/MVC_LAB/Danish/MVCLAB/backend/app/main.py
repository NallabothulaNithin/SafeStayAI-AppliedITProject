
from app.controllers.task_controller import router as task_router
from app.controllers.user_controller import router as user_router


from fastapi import FastAPI
app = FastAPI(title="MVCLAB backend API")
app.include_router(task_router, prefix="/tasks", tags=["tasks"])
app.include_router(user_router, prefix="/users", tags=["users"])
from fastapi.middleware.cors import CORSMiddleware
from app.controllers.task_controller  import router as task_router
from sqlalchemy import create_engine, text, select
from app.database import SessionLocal
from app.models import User
from app.controllers.auth_controller import router as auth_router
app.include_router(auth_router, prefix="/auth", tags=["auth"])
from app.auth.hashing import hash_password

import os

from app.database import Base, engine
from app import models

Base.metadata.create_all(bind=engine)




# the view runs on a different origin, so CROS is required
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.get("/db-ping")
# def db_ping():
#     engine = create_engine(os.environ["DATABASE_URL"])
#     with engine.connect() as conn:
#         return {"postgres": conn.execute(text("SELECT version()")).scalar()}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def seed_users():
    """Insert some users if the users table is empty."""
    with SessionLocal() as db:
        if db.scalars(select(User)).first() is not None:
            return
        db.add_all([User(name="Eshwaryadav", password_hash=hash_password("password123")),
                   User(name="Bob", password_hash=hash_password("password123"))])
        db.commit()

seed_users()                  

with SessionLocal() as db:
    users = db.scalars(select(User)).all()
    print(users)
    