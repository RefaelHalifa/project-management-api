from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.services import auth as auth_service

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new user account with full name, email and password. Password is hashed before storing — never stored in plain text."
)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = auth_service.register_user(db, user)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    return db_user

@router.post(
    "/login",
    response_model=Token,
    summary="Login and get access token",
    description="Login with email and password. Returns a JWT access token valid for 30 minutes. Include this token in the Authorization header as 'Bearer <token>' for all protected endpoints."
)
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    result = auth_service.login_user(
        db,
        email=user_credentials.email,
        password=user_credentials.password
    )
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return result