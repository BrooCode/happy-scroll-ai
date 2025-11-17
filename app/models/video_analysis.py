"""
Pydantic models for video analysis requests and responses.
"""
from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, Dict, Any


class VideoAnalysisRequest(BaseModel):
    """Request model for video analysis endpoint."""
    
    video_url: str = Field(
        ...,
        description="Video URL - can be Google Cloud Storage (gs://bucket/video.mp4) or YouTube URL",
        examples=[
            "gs://my-bucket/video.mp4",
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "https://youtu.be/dQw4w9WgXcQ",
            "https://www.youtube.com/shorts/abc123"
        ]
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
            }
        }


class VideoAnalysisResponse(BaseModel):
    """Response model for video analysis endpoint - Simplified version."""
    
    is_safe: bool = Field(
        ...,
        description="Whether the video content is safe for children according to strict Indian parenting norms"
    )
    
    reason: str = Field(
        ...,
        description="Detailed explanation from Gemini AI about the safety assessment"
    )
    
    gemini_verdict: str = Field(
        ...,
        description="Raw verdict from Gemini AI (YES if safe, NO if unsafe)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "is_safe": False,
                "reason": "The transcript contains the phrase \"sleeping naked,\" which, while presented in a health/sleep context, could be interpreted as suggestive and therefore inappropriate for children according to strict Indian family values. This violates the rule against nudity and sexual content references.",
                "gemini_verdict": "NO"
            }
        }


class VideoAnalysisError(BaseModel):
    """Error response model for video analysis."""
    
    error: str = Field(
        ...,
        description="Error message"
    )
    
    detail: Optional[str] = Field(
        None,
        description="Detailed error information"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "Transcription failed",
                "detail": "Could not access video at gs://bucket/video.mp4"
            }
        }
