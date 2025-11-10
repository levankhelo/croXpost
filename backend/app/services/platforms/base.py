"""
Base publisher class for platform integrations
"""
from abc import ABC, abstractmethod
from typing import Dict, Optional, List


class BasePlatformPublisher(ABC):
    """Base class for platform publishers"""
    
    def __init__(self, platform_account):
        """
        Initialize publisher with platform account
        
        Args:
            platform_account: PlatformAccount model instance
        """
        self.platform_account = platform_account
        self.access_token = platform_account.access_token
        self.refresh_token = platform_account.refresh_token
    
    @abstractmethod
    def publish(
        self,
        media_path: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> Dict:
        """
        Publish media to the platform
        
        Args:
            media_path: Path to media file
            title: Post title
            description: Post description
            tags: List of tags
        
        Returns:
            Dict with post_id and url
        """
        pass
    
    @abstractmethod
    def enable_monetization(self) -> bool:
        """
        Enable monetization for the account
        
        Returns:
            True if successful
        """
        pass
    
    def refresh_access_token(self):
        """Refresh the access token if needed"""
        # Platform-specific implementation
        pass
