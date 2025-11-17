"""
Pydantic models for moderation API requests and responses.
"""
from typing import Optional
from pydantic import BaseModel, Field, HttpUrl


class ModerationRequest(BaseModel):
    """Request model for image content moderation."""
    
    image_url: Optional[str] = Field(
        None,
        description="URL of the image/thumbnail to moderate",
        min_length=10,
        max_length=2048,
    )
    
    youtube_url: Optional[str] = Field(
        None,
        description="YouTube video URL to extract thumbnail and moderate",
        min_length=10,
        max_length=2048,
    )
    
    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "image_url": "https://example.com/thumbnail.jpg"
                },
                {
                    "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
                }
            ]
        }


class VideoModerationRequest(BaseModel):
    """Request model for video content moderation."""
    
    video_uri: str = Field(
        ...,
        description="Google Cloud Storage URI (gs://bucket/video.mp4) or HTTP(S) URL",
        min_length=10,
        max_length=2048,
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "video_uri": "gs://my-bucket/video.mp4"
            }
        }


class ModerationResponse(BaseModel):
    """Response model for content moderation results."""
    
    allowed: bool = Field(
        ...,
        description="Whether the content is allowed (safe, not flagged)",
    )
    safe: bool = Field(
        ...,
        description="Same as 'allowed'. Whether the content is safe (not flagged)",
    )
    reason: str = Field(
        ...,
        description="Explanation of why content is safe or unsafe",
    )
    categories: dict[str, bool] = Field(
        default_factory=dict,
        description="Dictionary of content categories with their flagged status",
    )
    likelihood_scores: Optional[dict[str, str]] = Field(
        default=None,
        description="Likelihood levels for each category (VERY_UNLIKELY, UNLIKELY, POSSIBLE, LIKELY, VERY_LIKELY)",
    )
    threshold: Optional[str] = Field(
        default=None,
        description="Threshold level used for moderation"
    )
    service: Optional[str] = Field(
        default="google_cloud_vision",
        description="Moderation service used"
    )
    thumbnail_url: Optional[str] = Field(
        default=None,
        description="Thumbnail URL (for YouTube videos)"
    )
    video_title: Optional[str] = Field(
        default=None,
        description="Video title (for YouTube videos)"
    )
    channel_title: Optional[str] = Field(
        default=None,
        description="Channel title (for YouTube videos)"
    )
    
    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "allowed": True,
                    "safe": True,
                    "reason": "Content is safe. No inappropriate content detected.",
                    "categories": {
                        "adult": False,
                        "violence": False,
                        "racy": False,
                        "medical": False,
                        "spoof": False
                    },
                    "likelihood_scores": {
                        "adult": "VERY_UNLIKELY",
                        "violence": "UNLIKELY",
                        "racy": "VERY_UNLIKELY",
                        "medical": "UNLIKELY",
                        "spoof": "VERY_UNLIKELY"
                    },
                    "threshold": "POSSIBLE",
                    "service": "google_cloud_vision"
                },
                {
                    "allowed": False,
                    "safe": False,
                    "reason": "Content flagged as UNSAFE. Detected: adult, racy.",
                    "categories": {
                        "adult": True,
                        "violence": False,
                        "racy": True,
                        "medical": False,
                        "spoof": False
                    },
                    "likelihood_scores": {
                        "adult": "LIKELY",
                        "violence": "UNLIKELY",
                        "racy": "POSSIBLE",
                        "medical": "UNLIKELY",
                        "spoof": "VERY_UNLIKELY"
                    },
                    "threshold": "POSSIBLE",
                    "service": "google_cloud_vision",
                    "thumbnail_url": "https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg",
                    "video_title": "Never Gonna Give You Up",
                    "channel_title": "Rick Astley"
                }
            ]
        }


class ErrorResponse(BaseModel):
    """Error response model."""
    
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "Invalid request",
                "detail": "Content field is required"
            }
        }
