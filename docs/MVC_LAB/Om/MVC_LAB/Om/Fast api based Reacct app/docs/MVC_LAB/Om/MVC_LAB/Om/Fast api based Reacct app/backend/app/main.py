from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from app.controllers.task_controller import router as task_router
import os
from app.database import Base, engine
from app import models  # noqa: F401 - registers Task with Base.metadata

app = FastAPI(title="MVC Task API")

Base.metadata.create_all(bind=engine) 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(task_router, prefix="/tasks", tags=["tasks"])


@app.get("/db-ping")
def db_ping():
    engine = create_engine(os.environ["DATABASE_URL"])

    with engine.connect() as conn:
        return {
            "postgres": conn.execute(
                text("SELECT version()")
            ).scalar()
        }