from pydantic import BaseModel
from typing import TypeVar, Generic, List

T = TypeVar("T")

class PaginationParams(BaseModel):
    """Reusable pagination parameters for all list endpoints"""
    page: int = 1      # Which page (starts at 1)
    limit: int = 10    # How many items per page

class PaginatedResponse(BaseModel, Generic[T]):
    """Standard paginated response wrapper"""
    items: List[T]          # The actual data
    total: int              # Total records in DB
    page: int               # Current page
    limit: int              # Items per page
    pages: int              # Total number of pages

    class Config:
        from_attributes = True