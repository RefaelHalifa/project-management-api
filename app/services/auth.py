from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.auth.utils import hash_password, verify_password, create_access_token

def get_user_by_email(db: Session, email: str):
    """Find a user by their email address"""
    return db.query(User).filter(User.email == email).first()

def register_user(db: Session, user: UserCreate):
    """
    Create a new user account.
    Hashes the password before storing — never store plain passwords.
    """
    # Check if email already exists
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        return None  # Route will handle the error response

    # Hash the password before saving
    hashed = hash_password(user.password)

    db_user = User(
        full_name=user.full_name,
        email=user.email,
        hashed_password=hashed
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def login_user(db: Session, email: str, password: str):
    """
    Verify credentials and return a JWT token if valid.
    Returns None if email not found or password is wrong.
    """
    # Step 1 — find the user
    user = get_user_by_email(db, email)
    if not user:
        return None

    # Step 2 — verify the password against the stored hash
    if not verify_password(password, user.hashed_password):
        return None

    # Step 3 — create and return a JWT token
    access_token = create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}