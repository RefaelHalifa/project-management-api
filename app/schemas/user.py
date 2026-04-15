from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# What the client sends when registering
class UserCreate(BaseModel):
    full_name: str
    email: str
    password: str  # plain password — we hash it before storing

# What we send back after register or when getting user info
class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# What the client sends when logging in
class UserLogin(BaseModel):
    email: str
    password: str

# What we send back after successful login
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# What's stored INSIDE the JWT token
class TokenData(BaseModel):
    user_id: Optional[int] = None