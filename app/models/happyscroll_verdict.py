"""
Pydantic models for HappyScroll combined verdict API.
"""
from pydantic import BaseModel, Field


class HappyScrollVerdictRequest(BaseModel):
    """Request model for combined video verdict."""
    
    video_url: str = Field(
        ...,
        description="YouTube video URL to analyze",
        min_length=10,
        max_length=2048,
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
            }
        }


class HappyScrollVerdictResponse(BaseModel):
    """Response model for combined video verdict."""
    
    is_safe_transcript: bool = Field(
        ...,
        description="Whether the video transcript/captions are safe (from video analysis)",
    )
    is_safe_thumbnail: bool = Field(
        ...,
        description="Whether the video thumbnail is safe (from moderation)",
    )
    is_safe: bool = Field(
        ...,
        description="Overall safety verdict (true only if both transcript and thumbnail are safe)",
    )
    transcript_reason: str = Field(
        ...,
        description="Detailed reason from transcript analysis",
    )
    thumbnail_reason: str = Field(
        ...,
        description="Detailed reason from thumbnail moderation",
    )
    overall_reason: str = Field(
        ...,
        description="Combined reason explaining the overall verdict",
    )
    video_title: str = Field(
        default=None,
        description="Video title from YouTube",
    )
    channel_title: str = Field(
        default=None,
        description="Channel name from YouTube",
    )
    
    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "is_safe_transcript": True,
                    "is_safe_thumbnail": True,
                    "is_safe": True,
                    "transcript_reason": "Content is educational and appropriate for children.",
                    "thumbnail_reason": "Content is safe. No inappropriate content detected.",
                    "overall_reason": "✅ SAFE: Both transcript and thumbnail are appropriate for children.",
                    "video_title": "Educational Kids Video",
                    "channel_title": "Kids Learning Channel"
                },
                {
                    "is_safe_transcript": False,
                    "is_safe_thumbnail": True,
                    "is_safe": False,
                    "transcript_reason": "UNSAFE - Contains adult themes and inappropriate language.",
                    "thumbnail_reason": "Content is safe. No inappropriate content detected.",
                    "overall_reason": "❌ UNSAFE: Transcript contains inappropriate content. Video should be blocked despite safe thumbnail.",
                    "video_title": "Adult Comedy Video",
                    "channel_title": "Comedy Channel"
                },
                {
                    "is_safe_transcript": True,
                    "is_safe_thumbnail": False,
                    "is_safe": False,
                    "transcript_reason": "Content is appropriate for children.",
                    "thumbnail_reason": "Content flagged as UNSAFE. Detected: adult, racy.",
                    "overall_reason": "❌ UNSAFE: Thumbnail contains inappropriate imagery. Video should be blocked despite safe transcript.",
                    "video_title": "Clickbait Video",
                    "channel_title": "Viral Channel"
                }
            ]
        }
