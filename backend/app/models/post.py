"""
Post model for cross-posting
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum as SQLEnum, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.core.database import Base


class PostStatus(str, enum.Enum):
    """Post status enumeration"""
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    PUBLISHING = "publishing"
    PUBLISHED = "published"
    FAILED = "failed"
    PARTIAL = "partial"  # Some platforms succeeded, others failed


class Post(Base):
    """Post model for cross-platform content"""
    
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    media_file_id = Column(Integer, ForeignKey("media_files.id"), nullable=False)
    title = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    tags = Column(JSON, nullable=True)  # List of tags
    status = Column(SQLEnum(PostStatus), default=PostStatus.DRAFT)
    scheduled_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="posts")
    media_file = relationship("MediaFile", back_populates="posts")
    platform_posts = relationship("PlatformPost", back_populates="post", cascade="all, delete-orphan")


class PlatformPost(Base):
    """Platform-specific post tracking"""
    
    __tablename__ = "platform_posts"
    
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    platform = Column(String, nullable=False)
    platform_post_id = Column(String, nullable=True)
    platform_url = Column(String, nullable=True)
    status = Column(String, nullable=False)  # success, failed, pending
    error_message = Column(Text, nullable=True)
    published_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    post = relationship("Post", back_populates="platform_posts")
