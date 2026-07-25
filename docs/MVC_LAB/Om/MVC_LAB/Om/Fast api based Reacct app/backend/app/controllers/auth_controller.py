from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from app.auth.hashing import hash_password, verify_password
from app.auth.tokens import create_access_token
from app.repositories.user_repository import UserRepository
from app.schemas import User as UserSchema
from app.controllers.task_controller import get_user_repo
from app.auth.dependencies import get_current_user
from app.models import User

router = APIRouter()

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class RegisterRequest(BaseModel):
    name: str
    password: str

@router.post("/register", response_model=UserSchema, status_code=201)
def register(payload: RegisterRequest, user_repo: UserRepository = Depends(get_user_repo)):
    """Register a new user."""
    if user_repo.find_by_name(payload.name):
        raise HTTPException(409,"Username already exists")
    return user_repo.add(name=payload.name, password_hash=hash_password(payload.password))


@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), user_repo: UserRepository = Depends(get_user_repo)):
    """Authenticate a user and return an access token."""
    user = user_repo.find_by_name(form_data.username)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = create_access_token(user.id)
    return TokenResponse(access_token=access_token)     


@router.get("/me", response_model=UserSchema)
def me(user: User = Depends(get_current_user)):
    """Return the currently authenticated user."""
    return user


