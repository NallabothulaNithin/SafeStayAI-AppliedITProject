from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from app.auth.hashing import hash_password, verify_password
from app.auth.tokens import create_access_token
from app.repositories.user_repositories import UserRepository
from app.schemas import User as UserSchema
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from app.auth.dependencies import get_current_user
from app.models import User


router = APIRouter()

def get_user_repo(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer" 

class RegisterRequest(BaseModel):
    name: str
    password: str


@router.post("/register", response_model=UserSchema, status_code=201)
def register(
    payload: RegisterRequest,
    repo: UserRepository = Depends(get_user_repo)
):
    pass


@router.post("/login", response_model=TokenResponse)
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    repo: UserRepository = Depends(get_user_repo)
):
    
    user = repo.find_by_name(form.username)

    print("Username:", form.username)
    print("User:", user)

    if user:
        print("Hash:", user.password_hash)
        print("Password valid:", verify_password(form.password, user.password_hash))

    if not user or not verify_password(form.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )


    access_token = create_access_token(user.id)
    return TokenResponse(access_token=access_token)     

@router.get("/me", response_model=UserSchema)
def me(user: User = Depends(get_current_user)):
    return user