"""
Platform Account model for storing OAuth tokens
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class PlatformAccount(Base):
    """Platform account model for OAuth integration"""
    
    __tablename__ = "platform_accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    platform = Column(String, nullable=False)  # tiktok, youtube, instagram, facebook, reddit, twitter, threads
    platform_user_id = Column(String, nullable=True)
    platform_username = Column(String, nullable=True)
    access_token = Column(Text, nullable=True)
    refresh_token = Column(Text, nullable=True)
    token_expires_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    monetization_enabled = Column(Boolean, default=False)
    platform_data = Column(JSON, nullable=True)  # Additional platform-specific data
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="platform_accounts")
