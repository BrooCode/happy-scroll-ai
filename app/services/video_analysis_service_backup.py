"""
Video Analysis Service
Handles video transcription using Google Cloud Speech-to-Text
and content safety analysis using Google Gemini AI.
Supports both Google Cloud Storage URLs and YouTube URLs (via caption extraction).
"""
import os
import time
import re
import html
import urllib.request
from typing import Dict, Any, Tuple
from pathlib import Path
from loguru import logger
from google.cloud import speech_v1 as speech
from google.cloud.speech_v1 import types
from google.cloud import storage
import google.generativeai as genai
import yt_dlp


class VideoAnalysisService:
    """
    Service for analyzing video content using Google Cloud Speech-to-Text
    and Gemini AI for safety assessment.
    """
    
    def __init__(
        self,
        credentials_path: str,
        project_id: str,
        gemini_api_key: str
    ):
        """
        Initialize the video analysis service.
        
        Args:
            credentials_path: Path to Google Cloud service account JSON key
            project_id: Google Cloud project ID
            gemini_api_key: API key for Google Gemini AI
        """
        self.credentials_path = credentials_path
        self.project_id = project_id
        self.gemini_api_key = gemini_api_key
        
        # Set Google Cloud credentials
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
        
        # Initialize Speech-to-Text client
        self.speech_client = speech.SpeechClient()
        
        # Initialize Gemini AI
        genai.configure(api_key=gemini_api_key)
        # Use gemini-2.0-flash (latest model)
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
    
    async def _extract_youtube_captions(self, youtube_url: str) -> Tuple[str, Dict[str, Any]]:
        """
        Extract captions/subtitles and metadata from YouTube video.
        Much faster than downloading and transcribing audio.
        
        Args:
            youtube_url: YouTube video URL
            
        Returns:
            Tuple of (captions_text, metadata)
            
        Raises:
            Exception: If caption extraction fails
        """
        logger.info(f"Extracting captions from YouTube: {youtube_url}")
        
        try:
            # Configure yt-dlp to only extract metadata and captions
            ydl_opts = {
                'skip_download': True,  # Don't download video/audio
                'writesubtitles': True,
                'writeautomaticsub': True,  # Get auto-generated captions if manual ones aren't available
                'subtitleslangs': ['en'],  # Prefer English
                'quiet': True,
                'no_warnings': True,
            }
            
            logger.debug(f"Extracting video info with yt-dlp...")
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Extract video information
                info = ydl.extract_info(youtube_url, download=False)
                
                # Get video metadata
                metadata = {
                    'title': info.get('title', 'Unknown'),
                    'description': info.get('description', ''),
                    'duration_seconds': info.get('duration', 0),
                    'uploader': info.get('uploader', 'Unknown'),
                    'upload_date': info.get('upload_date', ''),
                    'view_count': info.get('view_count', 0),
                    'like_count': info.get('like_count', 0),
                    'channel': info.get('channel', 'Unknown'),
                    'categories': info.get('categories', []),
                    'tags': info.get('tags', []),
                }
                
                logger.info(f"Video: {metadata['title']} ({metadata['duration_seconds']}s)")
                
                # Extract captions/subtitles
                captions_text = ""
                subtitles = info.get('subtitles', {})
                automatic_captions = info.get('automatic_captions', {})
                
                # Try to get captions in order of preference
                # 1. Manual English subtitles
                # 2. Automatic English captions
                # 3. Any available subtitles
                caption_data = None
                
                if 'en' in subtitles:
                    caption_data = subtitles['en']
                    logger.info("Using manual English subtitles")
                elif 'en' in automatic_captions:
                    caption_data = automatic_captions['en']
                    logger.info("Using auto-generated English captions")
                elif subtitles:
                    # Get first available subtitle
                    lang = list(subtitles.keys())[0]
                    caption_data = subtitles[lang]
                    logger.info(f"Using manual subtitles in language: {lang}")
                elif automatic_captions:
                    # Get first available auto-caption
                    lang = list(automatic_captions.keys())[0]
                    caption_data = automatic_captions[lang]
                    logger.info(f"Using auto-generated captions in language: {lang}")
                
                # Download and parse captions
                if caption_data:
                    # Find the best format (prefer vtt or json)
                    for fmt in caption_data:
                        if fmt.get('ext') in ['vtt', 'json3', 'srv3', 'srv2', 'srv1']:
                            caption_url = fmt.get('url')
                            if caption_url:
                                try:
                                    # Download captions
                                    import urllib.request
                                    with urllib.request.urlopen(caption_url) as response:
                                        caption_content = response.read().decode('utf-8')
                                        
                                        # Parse captions (simple text extraction)
                                        # Remove VTT headers and timestamps
                                        lines = caption_content.split('\n')
                                        text_lines = []
                                        for line in lines:
                                            line = line.strip()
                                            # Skip empty lines, timestamps, and VTT headers
                                            if line and not line.startswith('WEBVTT') and \
                                               not '-->' in line and not line.isdigit():
                                                # Remove HTML tags
                                                import html
                                                clean_line = html.unescape(line)
                                                clean_line = re.sub(r'<[^>]+>', '', clean_line)
                                                if clean_line:
                                                    text_lines.append(clean_line)
                                        
                                        captions_text = ' '.join(text_lines)
                                        logger.info(f"Extracted {len(captions_text)} characters of captions")
                                        break
                                except Exception as e:
                                    logger.warning(f"Failed to download captions from {caption_url}: {e}")
                                    continue
                
                if not captions_text:
                    # Fallback to description if no captions available
                    logger.warning("No captions available, using video description")
                    captions_text = metadata['description'] or "No captions or description available."
                
                # Calculate word count
                word_count = len(captions_text.split())
                metadata['word_count'] = word_count
                metadata['language'] = 'en'  # Assuming English for now
                metadata['source'] = 'youtube_captions'
                
                return captions_text, metadata
                
        except Exception as e:
            logger.error(f"Failed to extract YouTube captions: {str(e)}")
            raise Exception(f"Failed to extract YouTube captions: {str(e)}")
    
    async def transcribe_video(self, video_url: str) -> Tuple[str, Dict[str, Any]]:
        """
        Transcribe audio from a video using Google Cloud Speech-to-Text.
        Supports both Google Cloud Storage URLs and YouTube URLs.
        
        Args:
            video_url: Google Cloud Storage URL (gs://bucket/video.mp4) or YouTube URL
            
        Returns:
            Tuple of (transcript, metadata)
            
        Raises:
            ValueError: If video_url is invalid
            Exception: If transcription fails
        """
        # Check if it's a YouTube URL
        if self._is_youtube_url(video_url):
            logger.info(f"Detected YouTube URL: {video_url}")
            # Extract captions directly (much faster!)
            return await self._extract_youtube_captions(video_url)
        elif not video_url.startswith("gs://"):
            raise ValueError(
                f"Invalid video URL. Must be either a Google Cloud Storage URL (gs://) "
                f"or a YouTube URL. Got: {video_url}"
            )
        
        logger.info(f"Starting transcription for video: {video_url}")
        
        try:
            # Configure audio settings
            audio = speech.RecognitionAudio(uri=video_url)
            
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                # Try automatic detection first
                sample_rate_hertz=16000,
                language_code="en-US",
                # Enable automatic punctuation
                enable_automatic_punctuation=True,
                # Get word-level timestamps
                enable_word_time_offsets=True,
                # Use enhanced model for better accuracy
                use_enhanced=True,
                model="video",
                # Alternative language codes to try
                alternative_language_codes=["es-ES", "fr-FR", "de-DE"],
            )
            
            # Start long-running transcription
            logger.info("Submitting long-running transcription request...")
            operation = self.speech_client.long_running_recognize(
                config=config,
                audio=audio
            )
            
            # Wait for operation to complete (with timeout)
            logger.info("Waiting for transcription to complete (this may take a few minutes)...")
            response = operation.result(timeout=600)  # 10 minute timeout
            
            # Extract transcript and metadata
            transcript_parts = []
            total_confidence = 0.0
            confidence_count = 0
            duration_seconds = 0.0
            
            for result in response.results:
                # Get the most accurate alternative
                alternative = result.alternatives[0]
                transcript_parts.append(alternative.transcript)
                
                # Collect confidence scores
                if hasattr(alternative, 'confidence'):
                    total_confidence += alternative.confidence
                    confidence_count += 1
                
                # Get duration from word time offsets
                if alternative.words:
                    last_word = alternative.words[-1]
                    if hasattr(last_word, 'end_time'):
                        end_time = last_word.end_time.total_seconds()
                        if end_time > duration_seconds:
                            duration_seconds = end_time
            
            # Combine transcript
            full_transcript = " ".join(transcript_parts).strip()
            
            if not full_transcript:
                raise Exception("Transcription returned empty result. The video may not contain any speech.")
            
            # Calculate average confidence
            avg_confidence = total_confidence / confidence_count if confidence_count > 0 else 0.0
            
            # Prepare metadata
            metadata = {
                "duration_seconds": round(duration_seconds, 2),
                "language_code": config.language_code,
                "confidence": round(avg_confidence, 3),
                "word_count": len(full_transcript.split()),
                "character_count": len(full_transcript),
                "model": "video",
                "enhanced": True
            }
            
            logger.info(f"Transcription completed. Duration: {duration_seconds}s, Confidence: {avg_confidence:.2%}")
            logger.debug(f"Transcript preview: {full_transcript[:200]}...")
            
            return full_transcript, metadata
            
        except Exception as e:
            logger.error(f"Transcription failed: {str(e)}")
            raise Exception(f"Failed to transcribe video: {str(e)}")
    
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
        Complete video analysis pipeline: transcribe and analyze for safety.
        
        Args:
            video_url: Google Cloud Storage URL
            
        Returns:
            Dictionary with transcript, metadata, is_safe, reason, and verdict
            
        Raises:
            ValueError: If video_url is invalid
            Exception: If transcription or analysis fails
        """
        logger.info(f"Starting complete video analysis for: {video_url}")
        
        # Step 1: Transcribe video
        transcript, metadata = await self.transcribe_video(video_url)
        
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
        
        if not settings.google_application_credentials:
            raise ValueError("GOOGLE_APPLICATION_CREDENTIALS not set in environment")
        
        if not settings.gemini_api_key:
            raise ValueError("GEMINI_API_KEY not set in environment")
        
        _video_analysis_service = VideoAnalysisService(
            credentials_path=settings.google_application_credentials,
            project_id=settings.google_cloud_project,
            gemini_api_key=settings.gemini_api_key
        )
    
    return _video_analysis_service
