"""
Media File model
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, BigInteger, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.core.database import Base


class MediaType(str, enum.Enum):
    """Media type enumeration"""
    IMAGE = "image"
    VIDEO = "video"


class MediaFile(Base):
    """Media file model"""
    
    __tablename__ = "media_files"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    filename = Column(String, nullable=False)
    original_filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_size = Column(BigInteger, nullable=False)
    media_type = Column(SQLEnum(MediaType), nullable=False)
    mime_type = Column(String, nullable=False)
    duration = Column(Integer, nullable=True)  # For videos, in seconds
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    thumbnail_path = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="media_files")
    posts = relationship("Post", back_populates="media_file")
