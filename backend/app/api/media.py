"""
Media upload API routes
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
import os
import uuid
from datetime import datetime
import mimetypes

from app.core.database import get_db
from app.core.security import get_current_user
from app.core.config import settings
from app.models.user import User
from app.models.media import MediaFile, MediaType

router = APIRouter()


class MediaResponse(BaseModel):
    """Media file response schema"""
    id: int
    filename: str
    original_filename: str
    file_path: str
    file_size: int
    media_type: str
    mime_type: str
    duration: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    thumbnail_path: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


@router.post("/upload", response_model=MediaResponse)
async def upload_media(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Upload media file"""
    # Validate file extension
    file_ext = os.path.splitext(file.filename)[1].lower()
    
    if file_ext in settings.ALLOWED_VIDEO_EXTENSIONS:
        media_type = MediaType.VIDEO
    elif file_ext in settings.ALLOWED_IMAGE_EXTENSIONS:
        media_type = MediaType.IMAGE
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")
    
    # Generate unique filename
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)
    
    # Save file
    try:
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    
    # Get file size
    file_size = os.path.getsize(file_path)
    
    # Validate file size
    if file_size > settings.MAX_UPLOAD_SIZE:
        os.remove(file_path)
        raise HTTPException(status_code=400, detail="File size exceeds maximum allowed size")
    
    # Get mime type
    mime_type = mimetypes.guess_type(file.filename)[0] or "application/octet-stream"
    
    # Create media record
    media = MediaFile(
        user_id=current_user.id,
        filename=unique_filename,
        original_filename=file.filename,
        file_path=file_path,
        file_size=file_size,
        media_type=media_type,
        mime_type=mime_type
    )
    
    db.add(media)
    db.commit()
    db.refresh(media)
    
    return media


@router.get("/", response_model=List[MediaResponse])
async def list_media(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 50
):
    """List user's media files"""
    media_files = db.query(MediaFile).filter(
        MediaFile.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    
    return media_files


@router.get("/{media_id}", response_model=MediaResponse)
async def get_media(
    media_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get media file by ID"""
    media = db.query(MediaFile).filter(
        MediaFile.id == media_id,
        MediaFile.user_id == current_user.id
    ).first()
    
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")
    
    return media


@router.delete("/{media_id}")
async def delete_media(
    media_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete media file"""
    media = db.query(MediaFile).filter(
        MediaFile.id == media_id,
        MediaFile.user_id == current_user.id
    ).first()
    
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")
    
    # Delete file from filesystem
    if os.path.exists(media.file_path):
        os.remove(media.file_path)
    
    # Delete from database
    db.delete(media)
    db.commit()
    
    return {"message": "Media deleted successfully"}
