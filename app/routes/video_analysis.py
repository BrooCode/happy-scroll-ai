"""
Video Analysis API Routes
Endpoint for transcribing and analyzing video content for child safety.
"""
from fastapi import APIRouter, HTTPException, status
from loguru import logger

from app.models.video_analysis import (
    VideoAnalysisRequest,
    VideoAnalysisResponse,
    VideoAnalysisError
)
from app.services.video_analysis_service import get_video_analysis_service


router = APIRouter(prefix="/api", tags=["Video Analysis"])


@router.post(
    "/analyze_video",
    response_model=VideoAnalysisResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Video successfully analyzed",
            "model": VideoAnalysisResponse
        },
        400: {
            "description": "Invalid video URL",
            "model": VideoAnalysisError
        },
        500: {
            "description": "Transcription or analysis failed",
            "model": VideoAnalysisError
        }
    },
    summary="Analyze Video Content for Child Safety",
    description="""
    Analyzes YouTube video content using YouTube Data API and Gemini AI for strict child safety.
    
    **Supported Video Sources:**
    - YouTube URLs (youtube.com/watch, youtu.be, youtube.com/shorts, youtube.com/embed)
    
    **Process:**
    1. Extract video ID from YouTube URL
    2. Fetch video metadata via YouTube Data API (title, description, tags, duration)
    3. Fetch captions/subtitles via YouTube Captions API
    4. Analyze content with Gemini 2.0 Flash using STRICT Indian parenting norms
    5. Return safety assessment (is_safe, reason, gemini_verdict)
    
    **Requirements:**
    - YouTube API key must be configured (YOUTUBE_API_KEY)
    - Gemini API key must be set (GEMINI_API_KEY)
    
    **Example Requests:**
    ```json
    {
        "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    }
    ```
    
    ```json
    {
        "video_url": "gs://my-bucket/kids-video.mp4"
    }
    ```
    
    **Example Response (SAFE):**
    ```json
    {
        "is_safe": true,
        "reason": "Educational content appropriate for young children with no inappropriate elements.",
        "gemini_verdict": "YES"
    }
    ```
    
    **Example Response (UNSAFE):**
    ```json
    {
        "is_safe": false,
        "reason": "The transcript contains the phrase 'sleeping naked,' which, while presented in a health/sleep context, could be interpreted as suggestive and therefore inappropriate for children according to strict Indian family values. This violates the rule against nudity and sexual content references.",
        "gemini_verdict": "NO"
    }
    ```
    """
)
async def analyze_video(request: VideoAnalysisRequest):
    """
    Analyze YouTube video content for child safety using YouTube Data API and Gemini AI.
    
    Args:
        request: VideoAnalysisRequest with video_url
        
    Returns:
        VideoAnalysisResponse with is_safe, reason, and gemini_verdict
        
    Raises:
        HTTPException: If video URL is invalid or processing fails
    """
    video_url = request.video_url.strip()
    
    logger.info(f"Received video analysis request for: {video_url}")
    
    # Validate video URL format
    if not video_url:
        logger.warning("Empty video URL provided")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="video_url cannot be empty"
        )
    
    # Check if it's a valid YouTube URL
    is_youtube = any(domain in video_url.lower() for domain in ["youtube.com", "youtu.be"])
    
    if not is_youtube:
        logger.warning(f"Invalid video URL format: {video_url}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="video_url must be a YouTube URL (youtube.com, youtu.be, youtube.com/shorts, youtube.com/embed)"
        )
    
    try:
        # Get video analysis service
        service = get_video_analysis_service()
        
        # Perform complete analysis
        logger.info("Starting video analysis pipeline...")
        result = await service.analyze_video(video_url)
        
        # Create simplified response
        response = VideoAnalysisResponse(
            is_safe=result["is_safe"],
            reason=result["reason"],
            gemini_verdict=result["gemini_verdict"]
        )
        
        logger.info(
            f"Video analysis completed successfully. "
            f"Safe: {response.is_safe}"
        )
        
        return response
        
    except ValueError as e:
        # Handle validation errors
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
        
    except Exception as e:
        # Handle processing errors
        error_msg = str(e)
        logger.error(f"Video analysis failed: {error_msg}")
        
        # Determine error type
        if "youtube" in error_msg.lower() or "video id" in error_msg.lower():
            detail = f"YouTube extraction failed: {error_msg}"
        elif "caption" in error_msg.lower():
            detail = f"Caption extraction failed: {error_msg}"
        elif "gemini" in error_msg.lower() or "analysis" in error_msg.lower():
            detail = f"Content analysis failed: {error_msg}"
        else:
            detail = f"Processing failed: {error_msg}"
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )


@router.get(
    "/analyze_video/status",
    summary="Check Video Analysis Service Status",
    description="Check if the video analysis service is properly configured and ready",
    tags=["Video Analysis"]
)
async def check_video_analysis_status():
    """
    Check if video analysis service is properly configured.
    
    Returns:
        Status information about the service configuration
    """
    try:
        service = get_video_analysis_service()
        
        return {
            "status": "ready",
            "service": "video_analysis",
            "components": {
                "youtube_data_api": "configured",
                "gemini_ai": "configured"
            },
            "api_version": "youtube_v3"
        }
    except ValueError as e:
        return {
            "status": "not_configured",
            "error": str(e),
            "message": "Please set YOUTUBE_API_KEY and GEMINI_API_KEY in .env file"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }
