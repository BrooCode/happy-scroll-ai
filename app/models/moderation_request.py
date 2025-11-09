"""
Pydantic models for moderation API requests and responses.
"""
from typing import Optional
from pydantic import BaseModel, Field


class ModerationRequest(BaseModel):
    """Request model for content moderation."""
    
    content: str = Field(
        ...,
        description="The content to be moderated",
        min_length=1,
        max_length=10000,
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "content": "This is a sample text to moderate"
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
        description="Deprecated: Use 'allowed' instead. Whether the content is safe (not flagged)",
    )
    categories: dict[str, bool] = Field(
        default_factory=dict,
        description="Dictionary of content categories with their flagged status",
    )
    category_scores: Optional[dict[str, float]] = Field(
        default=None,
        description="Confidence scores for each category",
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "allowed": True,
                "safe": True,
                "categories": {
                    "violence": False,
                    "hate": False,
                    "sexual": False
                },
                "category_scores": {
                    "violence": 0.01,
                    "hate": 0.02,
                    "sexual": 0.01
                }
            }
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
