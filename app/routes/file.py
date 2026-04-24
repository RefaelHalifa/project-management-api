from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.services import file as file_service
import os

router = APIRouter(prefix="/tasks", tags=["Files"])

@router.post(
    "/{task_id}/upload",
    summary="Upload a file to a task",
    description="Upload a file attachment to a specific task. Allowed types: JPEG, PNG, GIF, PDF, TXT, DOC, DOCX. Maximum file size: 5MB."
)
def upload_file(
    task_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Upload a file attachment to a task"""
    # Validate file type — only allow safe file types
    allowed_types = [
        "image/jpeg", "image/png", "image/gif",
        "application/pdf",
        "text/plain",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type {file.content_type} not allowed"
        )

    # Validate file size — max 5MB
    file.file.seek(0, 2)              # seek to end of file
    file_size = file.file.tell()      # get file size in bytes
    file.file.seek(0)                 # reset to beginning
    if file_size > 5 * 1024 * 1024:  # 5MB in bytes
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size must be less than 5MB"
        )

    return file_service.save_file(task_id, file, db)

@router.get(
    "/{task_id}/file",
    summary="Get a presigned download link",
    description="Generate a temporary signed download URL for a task's file attachment. The link expires after 1 hour. No authentication needed to use the download link itself."
)
def get_file_link(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a presigned download link for a task's file"""
    return file_service.generate_presigned_link(task_id, db)

@router.get(
    "/{task_id}/download",
    summary="Download a file using presigned link",
    description="Download a task's file using a presigned URL. The URL must be valid and not expired. No authentication token required — the signature proves the link is legitimate."
)
def download_file(
    task_id: int,
    expires: int,
    signature: str,
    db: Session = Depends(get_db)
    # No auth needed — the signature proves the link is valid
):
    """Download a file using a presigned link"""
    file_path = file_service.verify_and_get_file(task_id, expires, signature, db)

    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found on server"
        )

    return FileResponse(
        path=file_path,
        filename=os.path.basename(file_path),
        media_type="application/octet-stream"
    )