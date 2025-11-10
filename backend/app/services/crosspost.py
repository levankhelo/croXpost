"""
Cross-posting service for publishing to multiple platforms
"""
from sqlalchemy.orm import Session
from datetime import datetime
import logging

from app.models.post import Post, PlatformPost, PostStatus
from app.models.platform_account import PlatformAccount
from app.models.media import MediaFile
from app.services.platforms.tiktok import TikTokPublisher
from app.services.platforms.youtube import YouTubePublisher
from app.services.platforms.instagram import InstagramPublisher
from app.services.platforms.facebook import FacebookPublisher
from app.services.platforms.reddit import RedditPublisher
from app.services.platforms.twitter import TwitterPublisher
from app.services.platforms.threads import ThreadsPublisher

logger = logging.getLogger(__name__)


# Platform publisher mapping
PLATFORM_PUBLISHERS = {
    "tiktok": TikTokPublisher,
    "youtube": YouTubePublisher,
    "instagram": InstagramPublisher,
    "facebook": FacebookPublisher,
    "reddit": RedditPublisher,
    "twitter": TwitterPublisher,
    "threads": ThreadsPublisher,
}


def publish_to_platforms(post_id: int, db: Session):
    """
    Publish a post to all selected platforms
    
    Args:
        post_id: ID of the post to publish
        db: Database session
    """
    # Get post
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        logger.error(f"Post {post_id} not found")
        return
    
    # Get media file
    media = db.query(MediaFile).filter(MediaFile.id == post.media_file_id).first()
    if not media:
        logger.error(f"Media file {post.media_file_id} not found")
        post.status = PostStatus.FAILED
        db.commit()
        return
    
    # Get platform posts
    platform_posts = db.query(PlatformPost).filter(PlatformPost.post_id == post_id).all()
    
    success_count = 0
    fail_count = 0
    
    for platform_post in platform_posts:
        # Get platform account
        platform_account = db.query(PlatformAccount).filter(
            PlatformAccount.user_id == post.user_id,
            PlatformAccount.platform == platform_post.platform,
            PlatformAccount.is_active == True
        ).first()
        
        if not platform_account:
            platform_post.status = "failed"
            platform_post.error_message = "Platform account not found or not active"
            fail_count += 1
            continue
        
        # Get publisher for platform
        publisher_class = PLATFORM_PUBLISHERS.get(platform_post.platform)
        if not publisher_class:
            platform_post.status = "failed"
            platform_post.error_message = f"No publisher implemented for {platform_post.platform}"
            fail_count += 1
            continue
        
        try:
            # Initialize publisher
            publisher = publisher_class(platform_account)
            
            # Publish to platform
            result = publisher.publish(
                media_path=media.file_path,
                title=post.title,
                description=post.description,
                tags=post.tags
            )
            
            # Update platform post
            platform_post.status = "success"
            platform_post.platform_post_id = result.get("post_id")
            platform_post.platform_url = result.get("url")
            platform_post.published_at = datetime.utcnow()
            success_count += 1
            
        except Exception as e:
            logger.error(f"Failed to publish to {platform_post.platform}: {str(e)}")
            platform_post.status = "failed"
            platform_post.error_message = str(e)
            fail_count += 1
    
    # Update overall post status
    if success_count > 0 and fail_count == 0:
        post.status = PostStatus.PUBLISHED
    elif success_count > 0 and fail_count > 0:
        post.status = PostStatus.PARTIAL
    else:
        post.status = PostStatus.FAILED
    
    db.commit()
    logger.info(f"Published post {post_id}: {success_count} succeeded, {fail_count} failed")
