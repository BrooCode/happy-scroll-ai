"""
Moderation API routes.
Handles content moderation requests from the Chrome extension.
"""
from fastapi import APIRouter, HTTPException, status
from openai import OpenAIError

from app.models.moderation_request import (
    ModerationRequest,
    ModerationResponse,
    ErrorResponse,
)
from app.services.openai_service import openai_service
from app.core.logger import logger

# Create router with prefix and tags
router = APIRouter(
    prefix="/api",
    tags=["moderation"],
)


@router.post(
    "/moderate",
    response_model=ModerationResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
    },
    summary="Moderate Content",
    description="Analyze content for safety using AI-based moderation",
)
async def moderate_content(request: ModerationRequest) -> ModerationResponse:
    """
    Moderate content using OpenAI's moderation API.
    
    Args:
        request: ModerationRequest containing the content to moderate
        
    Returns:
        ModerationResponse with safety status and flagged categories
        
    Raises:
        HTTPException: 400 for invalid requests, 500 for server errors
    """
    try:
        # Validate request
        if not request.content or not request.content.strip():
            logger.warning("Received empty content in moderation request")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Content cannot be empty",
            )
        
        # Call OpenAI service
        safe, flagged_categories_list, category_scores = await openai_service.moderate_content(
            request.content
        )
        
        # Build categories dictionary from scores
        categories_dict = {}
        if category_scores:
            for category, score in category_scores.items():
                categories_dict[category] = category in flagged_categories_list
        
        # Build response with both 'allowed' and 'safe' for backward compatibility
        response = ModerationResponse(
            allowed=safe,
            safe=safe,
            categories=categories_dict,
            category_scores=category_scores,
        )
        
        logger.info(
            f"Moderation request processed successfully - "
            f"Allowed: {safe}, Flagged categories: {flagged_categories_list}"
        )
        
        return response
        
    except OpenAIError as e:
        logger.error(f"OpenAI API error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"OpenAI API error: {str(e)}",
        )
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Unexpected error in moderation endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        )


@router.get(
    "/health",
    summary="Health Check",
    description="Check if the API is running",
    tags=["health"],
)
async def health_check():
    """
    Simple health check endpoint.
    
    Returns:
        Dict with status information
    """
    return {
        "status": "healthy",
        "service": "HappyScroll Moderation API",
        "version": "1.0.0",
    }
