from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controllers.task_controller import router as task_router

app = FastAPI(title="MY MVC Task API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],        
)
app.include_router(task_router, prefix="/tasks", tags=["tasks"])