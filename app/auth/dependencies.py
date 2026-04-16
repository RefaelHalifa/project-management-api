from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError
from app.database import get_db
from app.auth.utils import decode_access_token
from app.models.user import User
from app.schemas.user import TokenData

# HTTPBearer extracts the token from Authorization: Bearer <token>
# auto_error=False means we handle the error ourselves
security = HTTPBearer(auto_error=False)

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Extracts and validates the JWT token from the request header.
    Returns the current logged in user.
    Raises 401 if token is missing, invalid, or expired.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Check if credentials were provided at all
    if not credentials:
        raise credentials_exception

    try:
        # Extract the token from "Bearer <token>"
        token = credentials.credentials
        payload = decode_access_token(token)

        user_id: int = payload.get("user_id")
        if user_id is None:
            raise credentials_exception

        token_data = TokenData(user_id=user_id)

    except JWTError:
        raise credentials_exception

    # Find the user in the database
    user = db.query(User).filter(User.id == token_data.user_id).first()
    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )

    return user