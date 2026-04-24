from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.exceptions import HTTPException as FastAPIHTTPException
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import SQLAlchemyError

def generic_error_response(status_code: int, message: str) -> JSONResponse:
    """Standard error response format used across all handlers"""
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "error",
            "code": status_code,
            "message": message
        }
    )

async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    """
    Handles ALL HTTPExceptions — both from routes and from the framework.
    Provides friendly messages for common status codes.
    """
    # Override generic framework messages with friendly ones
    friendly_messages = {
        404: "The requested resource was not found",
        401: "Authentication required — please login",
        403: "You don't have permission to access this resource",
        405: "Method not allowed",
        500: "An unexpected error occurred. Please try again later."
    }

    # Use friendly message for generic framework errors
    # Keep specific messages from route-level HTTPExceptions
    detail = exc.detail
    if detail in ["Not Found", "Not found", "Method Not Allowed"]:
        # This is a generic framework message — replace with friendly one
        message = friendly_messages.get(exc.status_code, str(detail))
    else:
        # This is a specific route-level message — keep it as is
        message = str(detail)

    return generic_error_response(
        status_code=exc.status_code,
        message=message
    )

async def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    Handles 422 Validation errors.
    Extracts the first error message and returns it cleanly.
    """
    errors = exc.errors()
    first_error = errors[0]
    field = " → ".join(str(loc) for loc in first_error["loc"])
    message = f"Validation error on '{field}': {first_error['msg']}"

    return generic_error_response(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        message=message
    )

async def database_error_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    """Handles all database errors"""
    return generic_error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message="A database error occurred. Please try again later."
    )

async def internal_server_error_handler(request: Request, exc: Exception) -> JSONResponse:
    """Catch-all handler for any unexpected errors"""
    return generic_error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message="An unexpected error occurred. Please try again later."
    )