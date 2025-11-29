"""
HappyScroll Combined Verdict API Route
Combines video transcript analysis and thumbnail moderation for comprehensive safety verdict.
Uses parallel processing and caching for faster response times.

Rate Limiting: 150 NEW video analyses per day (cached videos excluded) - Demo version
"""
import asyncio
from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Request
from loguru import logger

from app.models.happyscroll_verdict import (
    HappyScrollVerdictRequest,
    HappyScrollVerdictResponse
)
from app.services.video_analysis_service import get_video_analysis_service
from app.services.youtube_service import get_youtube_service
from app.services.google_vision_service import get_vision_service
from app.services.cache_service import get_cache
from app.core.config import settings


router = APIRouter(prefix="/api/happyScroll/v1", tags=["HappyScroll Verdict"])


# Global rate limiting (resets when server restarts or at midnight)
# Only counts NEW video analysis (excludes cached results)
GLOBAL_DAILY_LIMIT = 150  # Total NEW video analyses per day across all users
GLOBAL_RESET_DATE = datetime.now().date()
GLOBAL_REQUEST_COUNT = 0


def check_global_limit(increment: bool = False):
    """
    Check if global daily limit has been reached
    
    Args:
        increment: If True, increment the counter (use for new video analysis only)
    
    Returns:
        dict: Rate limit information
    """
    global GLOBAL_REQUEST_COUNT, GLOBAL_RESET_DATE
    
    today = datetime.now().date()
    
    # Reset counter daily
    if today > GLOBAL_RESET_DATE:
        GLOBAL_REQUEST_COUNT = 0
        GLOBAL_RESET_DATE = today
        logger.info(f"🔄 Global rate limit reset for new day: {today}")
    
    # Check limit (before incrementing)
    if GLOBAL_REQUEST_COUNT >= GLOBAL_DAILY_LIMIT:
        logger.warning(f"⚠️ Global daily limit reached: {GLOBAL_REQUEST_COUNT}/{GLOBAL_DAILY_LIMIT}")
        raise HTTPException(
            status_code=429,
            detail={
                "error": "Daily limit exceeded",
                "message": "Demo API has reached its daily limit for new video analysis. Please try again tomorrow!",
                "info": "This is a demo project with limited free tier usage to manage costs.",
                "note": "Cached videos do not count toward the limit. For unlimited usage, deploy your own instance.",
                "limit": GLOBAL_DAILY_LIMIT,
                "requests_today": GLOBAL_REQUEST_COUNT
            }
        )
    
    # Increment only if requested (for new video analysis)
    if increment:
        GLOBAL_REQUEST_COUNT += 1
        logger.info(f"📊 NEW video analyses today: {GLOBAL_REQUEST_COUNT}/{GLOBAL_DAILY_LIMIT}")
    
    return {
        "requests_today": GLOBAL_REQUEST_COUNT,
        "limit": GLOBAL_DAILY_LIMIT,
        "remaining": GLOBAL_DAILY_LIMIT - GLOBAL_REQUEST_COUNT
    }


@router.get(
    "/cache/stats",
    status_code=status.HTTP_200_OK,
    summary="Get Cache Statistics",
    description="""
    Returns performance statistics for the verdict cache.
    
    **Metrics include:**
    - Cache hits and misses
    - Hit rate percentage
    - Number of cached entries
    - Time saved (in seconds and minutes)
    - Estimated cost savings
    
    **Use this to monitor cache effectiveness!**
    """
)
async def get_cache_statistics():
    """Get cache performance statistics"""
    cache = get_cache()
    stats = cache.get_stats()
    
    logger.info(f"📊 Cache stats requested: {stats['hit_rate_percentage']}% hit rate")
    
    return {
        "status": "success",
        "cache_statistics": stats,
        "message": f"Cache is {stats['hit_rate_percentage']}% effective"
    }


@router.post(
    "/cache/clear",
    status_code=status.HTTP_200_OK,
    summary="Clear Cache",
    description="""
    Clears all cached verdict results.
    
    **Use with caution:** This will force all subsequent requests to perform full analysis.
    """
)
async def clear_cache_endpoint():
    """Clear all cached results"""
    cache = get_cache()
    cleared_count = cache.clear()
    
    logger.warning(f"🗑️  Cache manually cleared: {cleared_count} entries removed")
    
    return {
        "status": "success",
        "message": "Cache cleared successfully",
        "entries_removed": cleared_count
    }


@router.post(
    "/verdict",
    response_model=HappyScrollVerdictResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Combined Video Safety Verdict",
    description="""
    **Comprehensive Video Safety Analysis with Parallel Processing & Caching**
    
    This endpoint combines two powerful moderation checks running simultaneously:
    1. **Transcript Analysis** - Analyzes video captions/transcript using Gemini AI with strict Indian parenting norms
    2. **Thumbnail Moderation** - Analyzes video thumbnail using Google Cloud Vision SafeSearch
    
    **Process (Parallel Execution with Cache):**
    1. Extracts video ID from YouTube URL
    2. **Checks cache first** - Returns instant response if video was analyzed before
    3. **If not cached, runs in parallel:**
       - Analyzes transcript/captions with Gemini AI (12 strict safety rules)
       - Fetches video metadata (title, channel, thumbnail) + analyzes thumbnail with Google Cloud Vision
    4. Combines results into overall safety verdict
    5. **Caches result** for 7 days
    
    **Performance:**
    - Cached videos: <1 second ⚡ (instant response)
    - New videos: 15-25 seconds (with parallel processing)
    - Cache hit rate: 60-80% for popular videos
    - Cache TTL: 7 days
    
    **Safety Rules:**
    - Video is SAFE only if BOTH transcript AND thumbnail are safe
    - Video is UNSAFE if EITHER transcript OR thumbnail is flagged
    - Provides detailed reasons for each check
    
    **Use Case:**
    Perfect for parental control apps and browser extensions that need comprehensive
    video safety assessment before allowing children to view content.
    
    **Example Use:**
    ```json
    {
      "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    }
    ```
    """,
)
async def get_video_verdict(request: HappyScrollVerdictRequest) -> HappyScrollVerdictResponse:
    """
    Get comprehensive safety verdict by analyzing both video transcript and thumbnail.
    
    Rate Limited: 150 NEW video analyses per day (cached videos don't count)
    
    Args:
        request: HappyScrollVerdictRequest with video_url
        
    Returns:
        HappyScrollVerdictResponse with combined safety analysis
        
    Raises:
        HTTPException: 400 for invalid URL, 429 for rate limit, 500 for processing errors
    """
    # Check rate limit (don't increment yet - only increment on cache MISS)
    limit_info = check_global_limit(increment=False)
    
    video_url = request.video_url.strip()
    
    logger.info("=" * 80)
    logger.info(f"HappyScroll Verdict Request: {video_url}")
    logger.info(f"📊 Rate Limit: {limit_info['requests_today']}/{limit_info['limit']} NEW videos ({limit_info['remaining']} remaining)")
    logger.info("=" * 80)
    
    # Validate video URL
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
            detail="video_url must be a YouTube URL (youtube.com, youtu.be, youtube.com/shorts)"
        )
    
    # Extract video ID for caching
    try:
        youtube_service = get_youtube_service(settings.youtube_api_key)
        video_id = youtube_service.extract_video_id(video_url)
        logger.info(f"📹 Video ID: {video_id}")
    except Exception as e:
        logger.error(f"Failed to extract video ID: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid YouTube URL: Could not extract video ID"
        )
    
    # =====================================
    # CHECK CACHE FIRST
    # =====================================
    cache = get_cache()
    cached_result = cache.get(video_id)
    
    if cached_result:
        logger.info("✅ CACHE HIT! Returning cached result (saved ~20 seconds)")
        logger.info("📊 Cache hit does NOT count toward rate limit")
        return HappyScrollVerdictResponse(**cached_result)
    
    logger.info("💫 Cache MISS - Performing full analysis...")
    
    # =====================================
    # INCREMENT RATE LIMIT COUNTER (only for new video analysis)
    # =====================================
    limit_info = check_global_limit(increment=True)
    logger.info(f"📈 Incremented rate limit counter: {limit_info['requests_today']}/{limit_info['limit']}")
    
    # Initialize variables
    transcript_safe = False
    thumbnail_safe = False
    transcript_reason = ""
    thumbnail_reason = ""
    video_title = ""
    channel_title = ""
    
    try:
        # =====================================
        # PARALLEL PROCESSING: Run both analyses simultaneously
        # =====================================
        logger.info("⚡ Running transcript and thumbnail analysis in parallel...")
        
        async def analyze_transcript():
            """Analyze video transcript with Gemini AI"""
            try:
                logger.info("🎬 Starting transcript analysis...")
                video_service = get_video_analysis_service()
                result = await video_service.analyze_video(video_url)
                
                safe = result.get("is_safe", False)
                reason = result.get("reason", "Analysis failed")
                
                logger.info(f"✅ Transcript Analysis Complete: Safe={safe}")
                return {"success": True, "safe": safe, "reason": reason}
                
            except ValueError as e:
                logger.error(f"Transcript validation error: {str(e)}")
                return {"success": False, "error": str(e), "type": "validation"}
            except Exception as e:
                logger.error(f"Transcript analysis failed: {str(e)}")
                return {"success": False, "error": str(e), "type": "processing"}
        
        async def analyze_thumbnail():
            """Analyze video thumbnail with Google Cloud Vision"""
            try:
                logger.info("🖼️  Starting thumbnail analysis...")
                
                # Get YouTube service
                if not settings.youtube_api_key:
                    raise ValueError("YouTube API key not configured")
                
                youtube_service = get_youtube_service(settings.youtube_api_key)
                
                # Extract video ID and get thumbnail + metadata
                video_id = youtube_service.extract_video_id(video_url)
                thumbnail_url, metadata = await youtube_service.analyze_youtube_video(video_url)
                
                title = metadata.get("title", "Unknown")
                channel = metadata.get("channel_title", "Unknown")
                
                logger.info(f"📹 Video: {title}")
                logger.info(f"📺 Channel: {channel}")
                logger.info(f"🖼️  Thumbnail: {thumbnail_url}")
                
                # Analyze thumbnail with Vision API
                vision_service = get_vision_service(settings.safety_threshold)
                thumbnail_result = await vision_service.analyze_content(thumbnail_url)
                
                safe = thumbnail_result.get("allowed", False)
                
                # Generate reason
                if safe:
                    reason = "Thumbnail is safe. No inappropriate content detected."
                else:
                    flagged = [cat for cat, flagged in thumbnail_result["categories"].items() if flagged]
                    reason = f"Thumbnail flagged as UNSAFE. Detected: {', '.join(flagged)}."
                
                logger.info(f"✅ Thumbnail Analysis Complete: Safe={safe}")
                
                return {
                    "success": True,
                    "safe": safe,
                    "reason": reason,
                    "title": title,
                    "channel": channel
                }
                
            except ValueError as e:
                logger.error(f"Thumbnail validation error: {str(e)}")
                return {"success": False, "error": str(e), "type": "validation"}
            except Exception as e:
                logger.error(f"Thumbnail analysis failed: {str(e)}")
                return {"success": False, "error": str(e), "type": "processing"}
        
        # Run both analyses in parallel
        logger.info("⚡ Launching parallel tasks...")
        transcript_task, thumbnail_task = await asyncio.gather(
            analyze_transcript(),
            analyze_thumbnail(),
            return_exceptions=False
        )
        
        logger.info("✅ Both analyses completed!")
        
        # Process transcript results
        if not transcript_task.get("success"):
            error_type = transcript_task.get("type", "processing")
            error_msg = transcript_task.get("error", "Unknown error")
            
            if error_type == "validation":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid YouTube URL: {error_msg}"
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Video transcript analysis failed: {error_msg}"
                )
        
        transcript_safe = transcript_task.get("safe", False)
        transcript_reason = transcript_task.get("reason", "Analysis failed")
        
        # Process thumbnail results
        if not thumbnail_task.get("success"):
            error_type = thumbnail_task.get("type", "processing")
            error_msg = thumbnail_task.get("error", "Unknown error")
            
            if error_type == "validation":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"YouTube metadata extraction failed: {error_msg}"
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Thumbnail moderation failed: {error_msg}"
                )
        
        thumbnail_safe = thumbnail_task.get("safe", False)
        thumbnail_reason = thumbnail_task.get("reason", "Analysis failed")
        video_title = thumbnail_task.get("title", "Unknown")
        channel_title = thumbnail_task.get("channel", "Unknown")
        
        # =====================================
        # COMBINE RESULTS
        # =====================================
        logger.info("🔍 Combining parallel results...")
        
        # Overall safety: BOTH must be safe
        overall_safe = transcript_safe and thumbnail_safe
        
        # Generate overall reason
        if overall_safe:
            overall_reason = "✅ SAFE: Both transcript and thumbnail are appropriate for children."
        elif not transcript_safe and not thumbnail_safe:
            overall_reason = (
                "❌ UNSAFE: Both transcript and thumbnail contain inappropriate content. "
                "Video should be blocked."
            )
        elif not transcript_safe:
            overall_reason = (
                "❌ UNSAFE: Transcript contains inappropriate content. "
                "Video should be blocked despite safe thumbnail."
            )
        else:  # not thumbnail_safe
            overall_reason = (
                "❌ UNSAFE: Thumbnail contains inappropriate imagery. "
                "Video should be blocked despite safe transcript."
            )
        
        logger.info("=" * 80)
        logger.info("🎯 FINAL VERDICT:")
        logger.info(f"   Overall Safe: {overall_safe}")
        logger.info(f"   Transcript Safe: {transcript_safe}")
        logger.info(f"   Thumbnail Safe: {thumbnail_safe}")
        logger.info(f"   Reason: {overall_reason}")
        logger.info("=" * 80)
        
        # Build response
        response = HappyScrollVerdictResponse(
            is_safe_transcript=transcript_safe,
            is_safe_thumbnail=thumbnail_safe,
            is_safe=overall_safe,
            transcript_reason=transcript_reason,
            thumbnail_reason=thumbnail_reason,
            overall_reason=overall_reason,
            video_title=video_title,
            channel_title=channel_title
        )
        
        # =====================================
        # CACHE THE RESULT
        # =====================================
        try:
            cache.set(video_id, response.dict())
            logger.info(f"💾 Result cached for video {video_id} (expires in 7 days)")
        except Exception as cache_error:
            logger.warning(f"Failed to cache result: {str(cache_error)}")
            # Don't fail the request if caching fails
        
        return response
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Unexpected error in verdict endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process video verdict: {str(e)}"
        )
