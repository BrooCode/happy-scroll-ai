"""
YouTube Data API service for extracting video metadata and thumbnails.
"""
import re
from typing import Dict, Optional, Tuple
import httpx
from app.core.logger import logger


class YouTubeService:
    """Service for fetching YouTube video metadata and thumbnails."""
    
    def __init__(self, api_key: str):
        """
        Initialize YouTube service.
        
        Args:
            api_key: YouTube Data API key
        """
        if not api_key:
            raise ValueError("YouTube API key is required")
        
        self.api_key = api_key
        self.base_url = "https://www.googleapis.com/youtube/v3"
        logger.info("YouTube service initialized")
    
    def extract_video_id(self, youtube_url: str) -> str:
        """
        Extract video ID from various YouTube URL formats.
        
        Supports:
        - https://www.youtube.com/watch?v=VIDEO_ID
        - https://youtu.be/VIDEO_ID
        - https://www.youtube.com/shorts/VIDEO_ID
        - https://www.youtube.com/embed/VIDEO_ID
        
        Args:
            youtube_url: YouTube video URL
            
        Returns:
            str: Video ID
            
        Raises:
            ValueError: If video ID cannot be extracted
        """
        logger.info(f"Extracting video ID from: {youtube_url}")
        
        # Patterns for different YouTube URL formats
        patterns = [
            r'(?:v=|/)([0-9A-Za-z_-]{11}).*',  # Standard and shortened URLs
            r'(?:embed/)([0-9A-Za-z_-]{11})',   # Embed URLs
            r'(?:shorts/)([0-9A-Za-z_-]{11})',  # Shorts URLs
        ]
        
        for pattern in patterns:
            match = re.search(pattern, youtube_url)
            if match:
                video_id = match.group(1)
                logger.info(f"Extracted video ID: {video_id}")
                return video_id
        
        raise ValueError(f"Could not extract video ID from URL: {youtube_url}")
    
    async def fetch_video_metadata(self, video_id: str) -> Dict:
        """
        Fetch video metadata from YouTube Data API.
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            dict: Video metadata containing title, channel, description, etc.
            
        Raises:
            Exception: If API call fails
        """
        logger.info(f"Fetching metadata for video: {video_id}")
        
        url = f"{self.base_url}/videos"
        params = {
            "part": "snippet",
            "id": video_id,
            "key": self.api_key
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params, timeout=10.0)
                response.raise_for_status()
                
                data = response.json()
                
                if not data.get("items"):
                    raise ValueError(f"Video not found: {video_id}")
                
                snippet = data["items"][0]["snippet"]
                
                metadata = {
                    "video_id": video_id,
                    "title": snippet.get("title", "Unknown"),
                    "channel_title": snippet.get("channelTitle", "Unknown"),
                    "description": snippet.get("description", ""),
                    "published_at": snippet.get("publishedAt", ""),
                    "tags": snippet.get("tags", []),
                }
                
                logger.info(f"Fetched metadata for: {metadata['title']}")
                return metadata
                
        except httpx.HTTPStatusError as e:
            logger.error(f"YouTube API HTTP error: {e.response.status_code} - {e.response.text}")
            raise Exception(f"YouTube API error: {e.response.status_code}")
        except Exception as e:
            logger.error(f"Error fetching video metadata: {str(e)}")
            raise
    
    def get_thumbnail_url(self, video_id: str, quality: str = "maxresdefault") -> str:
        """
        Get thumbnail URL for a video.
        
        Available qualities:
        - maxresdefault (1280x720) - not always available
        - hqdefault (480x360)
        - mqdefault (320x180)
        - default (120x90)
        
        Args:
            video_id: YouTube video ID
            quality: Thumbnail quality (maxresdefault, hqdefault, mqdefault, default)
            
        Returns:
            str: Thumbnail URL
        """
        thumbnail_url = f"https://i.ytimg.com/vi/{video_id}/{quality}.jpg"
        logger.info(f"Generated thumbnail URL: {thumbnail_url}")
        return thumbnail_url
    
    async def get_best_thumbnail_url(self, video_id: str) -> str:
        """
        Get the best available thumbnail URL (tries maxresdefault, falls back to hqdefault).
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            str: Best available thumbnail URL
        """
        logger.info(f"Finding best thumbnail for video: {video_id}")
        
        # Try maxresdefault first
        maxres_url = self.get_thumbnail_url(video_id, "maxresdefault")
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.head(maxres_url, timeout=5.0)
                if response.status_code == 200:
                    logger.info("Using maxresdefault thumbnail")
                    return maxres_url
        except Exception as e:
            logger.debug(f"maxresdefault not available: {str(e)}")
        
        # Fallback to hqdefault
        hq_url = self.get_thumbnail_url(video_id, "hqdefault")
        logger.info("Falling back to hqdefault thumbnail")
        return hq_url
    
    async def analyze_youtube_video(self, youtube_url: str) -> Tuple[str, Dict]:
        """
        Complete YouTube video analysis: extract ID, fetch metadata, get thumbnail.
        
        Args:
            youtube_url: YouTube video URL
            
        Returns:
            tuple: (thumbnail_url, metadata_dict)
            
        Raises:
            ValueError: If URL is invalid
            Exception: If API calls fail
        """
        logger.info(f"Starting YouTube video analysis for: {youtube_url}")
        
        # Step 1: Extract video ID
        video_id = self.extract_video_id(youtube_url)
        
        # Step 2: Fetch metadata
        metadata = await self.fetch_video_metadata(video_id)
        
        # Step 3: Get best thumbnail
        thumbnail_url = await self.get_best_thumbnail_url(video_id)
        
        logger.info(f"YouTube analysis complete. Thumbnail: {thumbnail_url}")
        return thumbnail_url, metadata


# Singleton instance
_youtube_service = None


def get_youtube_service(api_key: str = None) -> YouTubeService:
    """
    Get or create YouTube service singleton.
    
    Args:
        api_key: YouTube API key (required on first call)
        
    Returns:
        YouTubeService: Service instance
    """
    global _youtube_service
    
    if _youtube_service is None:
        if not api_key:
            raise ValueError("YouTube API key is required for first initialization")
        _youtube_service = YouTubeService(api_key)
    
    return _youtube_service
