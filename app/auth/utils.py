from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.config import settings

# Tell passlib to use bcrypt as our hashing algorithm
# bcrypt is the industry standard for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Convert a plain password into a bcrypt hash"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check if a plain password matches a stored hash"""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    """
    Create a JWT token containing the provided data.
    Automatically adds an expiry time.
    """
    to_encode = data.copy()

    # Token expires after X minutes (set in .env)
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    to_encode.update({"exp": expire})

    # Sign and encode the token using our secret key
    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm
    )
    return encoded_jwt

def decode_access_token(token: str) -> dict:
    """
    Decode and verify a JWT token.
    Returns the payload if valid, raises an error if not.
    """
    return jwt.decode(
        token,
        settings.secret_key,
        algorithms=[settings.algorithm]
    )