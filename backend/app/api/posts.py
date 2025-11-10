"""
Post/Cross-posting API routes
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.post import Post, PostStatus, PlatformPost
from app.models.media import MediaFile
from app.models.platform_account import PlatformAccount
from app.services.crosspost import publish_to_platforms

router = APIRouter()


class PostCreate(BaseModel):
    """Post creation schema"""
    media_file_id: int
    title: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    platforms: List[str]  # List of platform names to post to
    scheduled_at: Optional[datetime] = None


class PlatformPostResponse(BaseModel):
    """Platform post response schema"""
    platform: str
    status: str
    platform_url: Optional[str] = None
    error_message: Optional[str] = None
    
    class Config:
        from_attributes = True


class PostResponse(BaseModel):
    """Post response schema"""
    id: int
    title: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    status: str
    created_at: datetime
    platform_posts: List[PlatformPostResponse] = []
    
    class Config:
        from_attributes = True


@router.post("/", response_model=PostResponse)
async def create_post(
    post_data: PostCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create and publish a post to selected platforms"""
    # Validate media file
    media = db.query(MediaFile).filter(
        MediaFile.id == post_data.media_file_id,
        MediaFile.user_id == current_user.id
    ).first()
    
    if not media:
        raise HTTPException(status_code=404, detail="Media file not found")
    
    # Validate platforms are connected
    connected_platforms = db.query(PlatformAccount).filter(
        PlatformAccount.user_id == current_user.id,
        PlatformAccount.platform.in_(post_data.platforms),
        PlatformAccount.is_active == True
    ).all()
    
    connected_platform_names = [p.platform for p in connected_platforms]
    missing_platforms = set(post_data.platforms) - set(connected_platform_names)
    
    if missing_platforms:
        raise HTTPException(
            status_code=400,
            detail=f"Not connected to platforms: {', '.join(missing_platforms)}"
        )
    
    # Create post
    post = Post(
        user_id=current_user.id,
        media_file_id=post_data.media_file_id,
        title=post_data.title,
        description=post_data.description,
        tags=post_data.tags,
        status=PostStatus.PUBLISHING if not post_data.scheduled_at else PostStatus.SCHEDULED,
        scheduled_at=post_data.scheduled_at
    )
    
    db.add(post)
    db.commit()
    db.refresh(post)
    
    # Create platform post records
    for platform_name in post_data.platforms:
        platform_post = PlatformPost(
            post_id=post.id,
            platform=platform_name,
            status="pending"
        )
        db.add(platform_post)
    
    db.commit()
    
    # If not scheduled, publish immediately in background
    if not post_data.scheduled_at:
        background_tasks.add_task(
            publish_to_platforms,
            post.id,
            db
        )
    
    # Refresh to get platform_posts
    db.refresh(post)
    
    return post


@router.get("/", response_model=List[PostResponse])
async def list_posts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 50
):
    """List user's posts"""
    posts = db.query(Post).filter(
        Post.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    
    return posts


@router.get("/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get post by ID"""
    post = db.query(Post).filter(
        Post.id == post_id,
        Post.user_id == current_user.id
    ).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    return post


@router.delete("/{post_id}")
async def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a post"""
    post = db.query(Post).filter(
        Post.id == post_id,
        Post.user_id == current_user.id
    ).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    db.delete(post)
    db.commit()
    
    return {"message": "Post deleted successfully"}
