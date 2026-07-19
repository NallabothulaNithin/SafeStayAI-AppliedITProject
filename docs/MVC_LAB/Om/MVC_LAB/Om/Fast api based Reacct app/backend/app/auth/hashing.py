from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(plain: str) -> str:
    """Return a bcrypt hash of plaintext paassword."""
    return pwd_context.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    """verify a plaintext password against the stored hash"""
    return pwd_context.verify(plain, hashed)