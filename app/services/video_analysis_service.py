"""
Video Analysis Service - YouTube Data API Version
Handles video analysis using YouTube Data API for metadata and captions,
and Google Gemini AI for content safety analysis.
"""
import os
import re
import httpx
import html
from typing import Dict, Any, Tuple
from loguru import logger
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import google.generativeai as genai


class VideoAnalysisService:
    """
    Service for analyzing video content using YouTube Data API
    and Gemini AI for safety assessment.
    """
    
    def __init__(
        self,
        youtube_api_key: str,
        gemini_api_key: str
    ):
        """
        Initialize the VideoAnalysisService.
        
        Args:
            youtube_api_key: YouTube Data API key
            gemini_api_key: Google Gemini API key
            
        Raises:
            ValueError: If required credentials are missing
        """
        if not youtube_api_key:
            raise ValueError("YOUTUBE_API_KEY not found in environment")
        
        if not gemini_api_key:
            raise ValueError("GEMINI_API_KEY not found in environment")
        
        self.youtube_api_key = youtube_api_key
        
        # Initialize YouTube Data API client
        self.youtube = build('youtube', 'v3', developerKey=youtube_api_key)
        
        # Initialize Gemini AI
        genai.configure(api_key=gemini_api_key)
        self.gemini_model = genai.GenerativeModel('gemini-2.0-flash')
        
        logger.info("VideoAnalysisService initialized successfully")
    
    def _is_youtube_url(self, url: str) -> bool:
        """Check if URL is a YouTube URL."""
        youtube_patterns = [
            r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=[\w-]+',
            r'(?:https?://)?(?:www\.)?youtube\.com/shorts/[\w-]+',
            r'(?:https?://)?youtu\.be/[\w-]+',
            r'(?:https?://)?(?:www\.)?youtube\.com/embed/[\w-]+',
        ]
        return any(re.match(pattern, url) for pattern in youtube_patterns)
    
    def _extract_video_id(self, youtube_url: str) -> str:
        """
        Extract video ID from various YouTube URL formats.
        
        Args:
            youtube_url: YouTube video URL
            
        Returns:
            Video ID string
            
        Raises:
            ValueError: If video ID cannot be extracted
        """
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
    
    async def _fetch_video_metadata(self, video_id: str) -> Dict[str, Any]:
        """
        Fetch video metadata from YouTube Data API.
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            Dictionary containing video metadata
            
        Raises:
            Exception: If API call fails
        """
        try:
            logger.info(f"Fetching metadata for video: {video_id}")
            
            # Call YouTube Data API
            request = self.youtube.videos().list(
                part='snippet,contentDetails,statistics',
                id=video_id
            )
            response = request.execute()
            
            if not response.get('items'):
                raise Exception(f"Video not found: {video_id}")
            
            video = response['items'][0]
            snippet = video.get('snippet', {})
            statistics = video.get('statistics', {})
            content_details = video.get('contentDetails', {})
            
            # Parse ISO 8601 duration (e.g., PT1M30S = 90 seconds)
            duration_str = content_details.get('duration', 'PT0S')
            duration_seconds = self._parse_duration(duration_str)
            
            metadata = {
                'title': snippet.get('title', 'Unknown'),
                'description': snippet.get('description', ''),
                'duration_seconds': duration_seconds,
                'channel_title': snippet.get('channelTitle', 'Unknown'),
                'publish_date': snippet.get('publishedAt', ''),
                'view_count': int(statistics.get('viewCount', 0)),
                'like_count': int(statistics.get('likeCount', 0)),
                'tags': snippet.get('tags', []),
                'category_id': snippet.get('categoryId', ''),
                'source': 'youtube_data_api'
            }
            
            logger.info(f"Video: {metadata['title']} ({metadata['duration_seconds']}s)")
            return metadata
            
        except HttpError as e:
            logger.error(f"YouTube API error: {e}")
            raise Exception(f"Failed to fetch video metadata: {e}")
        except Exception as e:
            logger.error(f"Error fetching metadata: {e}")
            raise
    
    def _parse_duration(self, duration_str: str) -> int:
        """
        Parse ISO 8601 duration to seconds.
        
        Args:
            duration_str: ISO 8601 duration string (e.g., PT1H2M30S)
            
        Returns:
            Duration in seconds
        """
        import re
        
        # Remove PT prefix
        duration_str = duration_str.replace('PT', '')
        
        hours = 0
        minutes = 0
        seconds = 0
        
        # Extract hours
        hours_match = re.search(r'(\d+)H', duration_str)
        if hours_match:
            hours = int(hours_match.group(1))
        
        # Extract minutes
        minutes_match = re.search(r'(\d+)M', duration_str)
        if minutes_match:
            minutes = int(minutes_match.group(1))
        
        # Extract seconds
        seconds_match = re.search(r'(\d+)S', duration_str)
        if seconds_match:
            seconds = int(seconds_match.group(1))
        
        total_seconds = hours * 3600 + minutes * 60 + seconds
        return total_seconds
    
    async def _fetch_captions(self, video_id: str) -> str:
        """
        Fetch captions/subtitles from YouTube video using httpx.
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            Caption text as string
            
        Raises:
            Exception: If caption fetching fails
        """
        try:
            logger.info(f"Fetching captions for video: {video_id}")
            
            # First, list available captions
            request = self.youtube.captions().list(
                part='snippet',
                videoId=video_id
            )
            response = request.execute()
            
            if not response.get('items'):
                logger.warning("No captions available for this video")
                return ""
            
            # Find English caption track (prefer manual over auto-generated)
            caption_id = None
            for item in response['items']:
                snippet = item.get('snippet', {})
                language = snippet.get('language', '')
                track_kind = snippet.get('trackKind', '')
                
                if language == 'en':
                    if track_kind == 'standard':
                        caption_id = item['id']
                        logger.info("Using manual English captions")
                        break
                    elif track_kind == 'asr':
                        caption_id = item['id']
                        logger.info("Using auto-generated English captions")
            
            # If no English captions, use the first available
            if not caption_id and response['items']:
                caption_id = response['items'][0]['id']
                lang = response['items'][0]['snippet'].get('language', 'unknown')
                logger.info(f"Using first available caption track: {lang}")
            
            if not caption_id:
                return ""
            
            # Download caption using YouTube's timedtext API (workaround)
            # Note: Official captions().download() requires OAuth, so we use timedtext
            timedtext_url = f"https://www.youtube.com/api/timedtext?v={video_id}&lang=en&fmt=vtt"
            
            async with httpx.AsyncClient() as client:
                response = await client.get(timedtext_url, timeout=30.0)
                response.raise_for_status()
                
                caption_content = response.text
                
                # Parse VTT format to extract text
                lines = caption_content.split('\n')
                text_lines = []
                
                for line in lines:
                    line = line.strip()
                    # Skip empty lines, WEBVTT headers, timestamps
                    if line and not line.startswith('WEBVTT') and '-->' not in line and not line.isdigit():
                        # Remove HTML tags
                        clean_line = re.sub(r'<[^>]+>', '', line)
                        if clean_line:
                            text_lines.append(clean_line)
                
                captions_text = ' '.join(text_lines)
                logger.info(f"Extracted {len(captions_text)} characters of captions")
                
                return captions_text
                
        except HttpError as e:
            logger.warning(f"YouTube API error fetching captions: {e}")
            return ""
        except Exception as e:
            logger.warning(f"Failed to fetch captions: {e}")
            return ""
    
    async def _extract_youtube_captions(self, youtube_url: str) -> Tuple[str, Dict[str, Any]]:
        """
        Extract captions/subtitles and metadata from YouTube video using YouTube Data API.
        
        Args:
            youtube_url: YouTube video URL
            
        Returns:
            Tuple of (captions_text, metadata)
            
        Raises:
            Exception: If extraction fails
        """
        logger.info(f"Extracting data from YouTube: {youtube_url}")
        
        try:
            # Extract video ID from URL
            video_id = self._extract_video_id(youtube_url)
            
            # Fetch metadata from YouTube Data API
            metadata = await self._fetch_video_metadata(video_id)
            
            # Fetch captions from YouTube
            captions_text = await self._fetch_captions(video_id)
            
            # If no captions, fall back to description
            if not captions_text:
                logger.warning("No captions available, using video description")
                captions_text = metadata.get('description', '') or "No captions or description available."
            
            # Add word count
            word_count = len(captions_text.split())
            metadata['word_count'] = word_count
            metadata['language'] = 'en'
            
            logger.info(f"Successfully extracted {len(captions_text)} characters from video")
            return captions_text, metadata
                
        except Exception as e:
            logger.error(f"Failed to extract YouTube data: {str(e)}")
            raise Exception(f"Failed to extract YouTube data: {str(e)}")
    

    
    async def analyze_with_gemini(
        self,
        transcript: str,
        metadata: Dict[str, Any]
    ) -> Tuple[bool, str, str]:
        """
        Analyze transcript using Gemini AI to determine if content is safe for kids.
        
        Args:
            transcript: Full video transcript
            metadata: Video metadata dictionary
            
        Returns:
            Tuple of (is_safe, reason, verdict)
            
        Raises:
            Exception: If Gemini analysis fails
        """
        logger.info("Analyzing content safety with Gemini AI...")
        
        try:
            # Construct the prompt - STRICT Indian parenting norms
            prompt = f"""You are a content moderator following STRICT Indian parenting norms for children's safety.

Analyze this video transcript and metadata:

TRANSCRIPT:
{transcript}

METADATA:
{metadata}

STRICT SAFETY RULES (ANY violation = UNSAFE):

🚫 ABSOLUTELY NOT ALLOWED (Mark as UNSAFE):
1. Nudity - ANY form (partial, full, artistic, medical, accidental, cartoon)
2. Sexual Content - ANY references (innuendos, jokes, gestures, educational)
3. Racism - ANY form (jokes, stereotypes, slurs, casual references)
4. Discrimination - Based on religion, caste, gender, region, color
5. Violence - Physical harm, weapons, blood, fighting, bullying
6. Abusive Language - Swear words, profanity, insults, derogatory terms
7. Drugs/Alcohol - Any references, jokes, or depiction
8. Scary Content - Horror, gore, disturbing imagery
9. Inappropriate Gestures - Offensive hand signs, provocative movements
10. Adult Themes - Dating, romance, intimate situations
11. Dangerous Acts - Stunts, risky behavior kids might copy
12. Religious Insensitivity - Mocking any faith or belief

✅ SAFE ONLY IF:
- Educational and age-appropriate
- Positive, uplifting messages
- Family-friendly entertainment
- Cultural content respectful to all
- No questionable elements whatsoever

IMPORTANT: Follow strict Indian family values. When in doubt, mark as UNSAFE. Better to be over-cautious than risk exposing children to inappropriate content.

Respond EXACTLY in this format:
VERDICT: [YES if completely safe, NO if any concern]
EXPLANATION: [Detailed explanation of your decision]
"""
            
            # Generate response from Gemini
            logger.debug(f"Sending prompt to Gemini (transcript length: {len(transcript)} chars)")
            response = self.gemini_model.generate_content(prompt)
            
            # Extract response text
            response_text = response.text.strip()
            logger.debug(f"Gemini response: {response_text}")
            
            # Parse verdict and explanation
            verdict_match = re.search(r'VERDICT:\s*(YES|NO)', response_text, re.IGNORECASE)
            explanation_match = re.search(r'EXPLANATION:\s*(.+)', response_text, re.IGNORECASE | re.DOTALL)
            
            if not verdict_match:
                # Fallback: look for YES or NO anywhere in response
                if re.search(r'\bYES\b', response_text, re.IGNORECASE):
                    verdict = "YES"
                elif re.search(r'\bNO\b', response_text, re.IGNORECASE):
                    verdict = "NO"
                else:
                    raise Exception("Could not parse verdict from Gemini response")
            else:
                verdict = verdict_match.group(1).upper()
            
            # Extract explanation
            if explanation_match:
                reason = explanation_match.group(1).strip()
            else:
                # Use entire response as reason if no clear format
                reason = response_text
            
            # Determine safety
            is_safe = verdict == "YES"
            
            logger.info(f"Gemini analysis complete. Verdict: {verdict}, Is Safe: {is_safe}")
            
            return is_safe, reason, verdict
            
        except Exception as e:
            logger.error(f"Gemini analysis failed: {str(e)}")
            raise Exception(f"Failed to analyze content with Gemini: {str(e)}")
    
    async def analyze_video(self, video_url: str) -> Dict[str, Any]:
        """
        Complete video analysis pipeline: extract captions and analyze for safety.
        
        Args:
            video_url: YouTube video URL (regular, shorts, or embed format)
            
        Returns:
            Dictionary with is_safe, reason, and gemini_verdict
            
        Raises:
            ValueError: If video_url is not a valid YouTube URL
            Exception: If extraction or analysis fails
        """
        logger.info(f"Starting video analysis for: {video_url}")
        
        # Validate YouTube URL
        if not self._is_youtube_url(video_url):
            raise ValueError(
                f"Invalid video URL. Must be a YouTube URL. Got: {video_url}"
            )
        
        # Step 1: Extract captions and metadata
        transcript, metadata = await self._extract_youtube_captions(video_url)
        
        # Step 2: Analyze with Gemini
        is_safe, reason, verdict = await self.analyze_with_gemini(transcript, metadata)
        
        # Step 3: Return simplified result (only safety information)
        result = {
            "is_safe": is_safe,
            "reason": reason,
            "gemini_verdict": verdict
        }
        
        logger.info(f"Video analysis complete. Safe: {is_safe}")
        
        return result


# Singleton instance
_video_analysis_service = None


def get_video_analysis_service() -> VideoAnalysisService:
    """
    Get or create the singleton VideoAnalysisService instance.
    
    Returns:
        VideoAnalysisService instance
    """
    global _video_analysis_service
    
    if _video_analysis_service is None:
        from app.core.config import settings
        
        if not settings.youtube_api_key:
            raise ValueError("YOUTUBE_API_KEY not set in environment")
        
        if not settings.gemini_api_key:
            raise ValueError("GEMINI_API_KEY not set in environment")
        
        _video_analysis_service = VideoAnalysisService(
            youtube_api_key=settings.youtube_api_key,
            gemini_api_key=settings.gemini_api_key
        )
    
    return _video_analysis_service
