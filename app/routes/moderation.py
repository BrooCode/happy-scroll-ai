"""
Moderation API routes.
Handles content moderation requests from the Chrome extension using Google Cloud Vision API.
"""
from fastapi import APIRouter, HTTPException, status

from app.models.moderation_request import (
    ModerationRequest,
    VideoModerationRequest,
    ModerationResponse,
    ErrorResponse,
)
from app.services.google_vision_service import get_vision_service
from app.services.google_video_service import get_video_service
from app.core.config import settings
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
    summary="Moderate Image or YouTube Video Content",
    description="""
    Analyze image/thumbnail or YouTube video for safety using Google Cloud Vision SafeSearch API.
    
    **Two modes:**
    1. **Direct Image Moderation**: Pass `image_url` to analyze any image
    2. **YouTube Video Moderation**: Pass `youtube_url` to extract thumbnail and analyze
    
    **YouTube Mode Process:**
    - Extract video ID from YouTube URL
    - Fetch video metadata (title, channel) via YouTube Data API v3
    - Get best quality thumbnail (maxresdefault or hqdefault)
    - Analyze thumbnail with Google Cloud Vision SafeSearch
    - Return moderation result with video metadata
    
    **Safety Categories Checked:**
    - Adult content
    - Violence
    - Racy content
    - Medical content
    - Spoof content
    """,
)
async def moderate_content(request: ModerationRequest) -> ModerationResponse:
    """
    Moderate image or YouTube video content using Google Cloud Vision SafeSearch API.
    
    This endpoint supports two modes:
    1. Direct image moderation (pass image_url)
    2. YouTube video thumbnail moderation (pass youtube_url)
    
    Args:
        request: ModerationRequest containing either image_url or youtube_url
        
    Returns:
        ModerationResponse with safety status, flagged categories, and reason
        
    Raises:
        HTTPException: 400 for invalid requests, 500 for server errors
    """
    try:
        # Validate request - must have either image_url or youtube_url
        if not request.image_url and not request.youtube_url:
            logger.warning("No image_url or youtube_url provided")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Either image_url or youtube_url must be provided",
            )
        
        if request.image_url and request.youtube_url:
            logger.warning("Both image_url and youtube_url provided")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Provide either image_url or youtube_url, not both",
            )
        
        # Get Vision service
        vision_service = get_vision_service(settings.safety_threshold)
        
        # Initialize response variables
        thumbnail_url = None
        video_title = None
        channel_title = None
        image_url_to_analyze = None
        
        # YouTube URL mode
        if request.youtube_url:
            logger.info(f"YouTube mode: Processing {request.youtube_url}")
            
            # Import YouTube service
            from app.services.youtube_service import get_youtube_service
            
            # Validate YouTube API key
            if not settings.youtube_api_key:
                logger.error("YouTube API key not configured")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="YouTube API key not configured. Set YOUTUBE_API_KEY in environment.",
                )
            
            try:
                # Get YouTube service
                youtube_service = get_youtube_service(settings.youtube_api_key)
                
                # Extract video ID, fetch metadata, and get thumbnail
                thumbnail_url, metadata = await youtube_service.analyze_youtube_video(request.youtube_url)
                
                video_title = metadata.get("title")
                channel_title = metadata.get("channel_title")
                image_url_to_analyze = thumbnail_url
                
                logger.info(f"YouTube video: {video_title} by {channel_title}")
                logger.info(f"Analyzing thumbnail: {thumbnail_url}")
                
            except ValueError as e:
                logger.error(f"Invalid YouTube URL: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid YouTube URL: {str(e)}",
                )
            except Exception as e:
                logger.error(f"YouTube API error: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to fetch YouTube data: {str(e)}",
                )
        else:
            # Direct image URL mode
            logger.info(f"Image mode: Processing {request.image_url}")
            image_url_to_analyze = request.image_url.strip()
        
        # Analyze image content with Vision API
        logger.info(f"Analyzing content with Google Vision API: {image_url_to_analyze}")
        analysis_result = await vision_service.analyze_content(image_url_to_analyze)
        
        # Generate human-readable reason
        is_safe = analysis_result["allowed"]
        flagged_categories = [cat for cat, flagged in analysis_result["categories"].items() if flagged]
        
        if is_safe:
            reason = "Content is safe. No inappropriate content detected."
        else:
            reason = f"Content flagged as UNSAFE. Detected: {', '.join(flagged_categories)}."
        
        # Build response
        response = ModerationResponse(
            allowed=is_safe,
            safe=is_safe,
            reason=reason,
            categories=analysis_result["categories"],
            likelihood_scores=analysis_result["likelihood_scores"],
            threshold=analysis_result["threshold"],
            service=analysis_result["service"],
            thumbnail_url=thumbnail_url,
            video_title=video_title,
            channel_title=channel_title
        )
        
        logger.info(
            f"Moderation complete - Safe: {response.safe} | "
            f"Reason: {reason} | "
            f"Source: {'YouTube' if request.youtube_url else 'Direct Image'}"
        )
        
        return response
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Unexpected error in moderation endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        )


@router.post(
    "/moderate/video",
    response_model=dict,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
    },
    summary="Moderate Video Content (Advanced)",
    description="Analyze full video for explicit content using Google Cloud Video Intelligence API (takes 1-5 minutes)",
)
async def moderate_video(request: VideoModerationRequest) -> dict:
    """
    Moderate video content using Google Cloud Video Intelligence API.
    
    Note: This is an advanced feature that takes 1-5 minutes to complete.
    Best used for pre-processing or background tasks, not real-time filtering.
    
    Args:
        request: VideoModerationRequest containing the video_uri to moderate
        
    Returns:
        dict with video analysis results
        
    Raises:
        HTTPException: 400 for invalid requests, 500 for server errors
    """
    try:
        if not request.video_uri or not request.video_uri.strip():
            logger.warning("Received empty video_uri in video moderation request")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="video_uri cannot be empty",
            )
        
        # Get Video service
        video_service = get_video_service()
        
        # Analyze video
        logger.info("Starting video analysis (this may take several minutes)...")
        analysis_result = await video_service.analyze_video_explicit_content(request.video_uri)
        
        logger.info(f"Video moderation complete: Safe={analysis_result['safe']}")
        
        return analysis_result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in video moderation endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Video moderation error: {str(e)}",
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
