"""
Platform integration API routes
"""
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.platform_account import PlatformAccount

router = APIRouter()


class PlatformAccountResponse(BaseModel):
    """Platform account response schema"""
    id: int
    platform: str
    platform_username: Optional[str] = None
    is_active: bool
    monetization_enabled: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class PlatformConnect(BaseModel):
    """Platform connection schema"""
    platform: str
    access_token: str
    refresh_token: Optional[str] = None
    platform_user_id: Optional[str] = None
    platform_username: Optional[str] = None


@router.get("/", response_model=List[PlatformAccountResponse])
async def list_platforms(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List user's connected platforms"""
    platforms = db.query(PlatformAccount).filter(
        PlatformAccount.user_id == current_user.id
    ).all()
    
    return platforms


@router.post("/connect", response_model=PlatformAccountResponse)
async def connect_platform(
    platform_data: PlatformConnect,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Connect a platform account"""
    # Check if platform already connected
    existing = db.query(PlatformAccount).filter(
        PlatformAccount.user_id == current_user.id,
        PlatformAccount.platform == platform_data.platform
    ).first()
    
    if existing:
        # Update existing connection
        existing.access_token = platform_data.access_token
        existing.refresh_token = platform_data.refresh_token
        existing.platform_user_id = platform_data.platform_user_id
        existing.platform_username = platform_data.platform_username
        existing.is_active = True
        db.commit()
        db.refresh(existing)
        return existing
    
    # Create new platform account
    platform_account = PlatformAccount(
        user_id=current_user.id,
        platform=platform_data.platform,
        access_token=platform_data.access_token,
        refresh_token=platform_data.refresh_token,
        platform_user_id=platform_data.platform_user_id,
        platform_username=platform_data.platform_username,
        is_active=True
    )
    
    db.add(platform_account)
    db.commit()
    db.refresh(platform_account)
    
    return platform_account


@router.delete("/{platform_id}")
async def disconnect_platform(
    platform_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Disconnect a platform account"""
    platform = db.query(PlatformAccount).filter(
        PlatformAccount.id == platform_id,
        PlatformAccount.user_id == current_user.id
    ).first()
    
    if not platform:
        raise HTTPException(status_code=404, detail="Platform not found")
    
    db.delete(platform)
    db.commit()
    
    return {"message": "Platform disconnected successfully"}


@router.post("/{platform_id}/monetization")
async def enable_monetization(
    platform_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Enable monetization for a platform"""
    platform = db.query(PlatformAccount).filter(
        PlatformAccount.id == platform_id,
        PlatformAccount.user_id == current_user.id
    ).first()
    
    if not platform:
        raise HTTPException(status_code=404, detail="Platform not found")
    
    # Here you would implement platform-specific monetization API calls
    # For now, just toggle the flag
    platform.monetization_enabled = True
    db.commit()
    db.refresh(platform)
    
    return {"message": "Monetization enabled successfully", "platform": platform.platform}
