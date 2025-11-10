"""
Database initialization script
"""
from app.core.database import Base, engine
from app.models.user import User
from app.models.platform_account import PlatformAccount
from app.models.media import MediaFile
from app.models.post import Post, PlatformPost

def init_db():
    """Initialize database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_db()
