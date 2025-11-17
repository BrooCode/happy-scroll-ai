"""
Google Cloud Video Intelligence API service for video content moderation.
Analyzes full videos for explicit content detection (optional, advanced feature).
"""

from typing import Dict, List
from app.core.logger import logger

from google.cloud import videointelligence_v1 as videointelligence


class GoogleVideoService:
    """Service for analyzing video content safety using Google Cloud Video Intelligence API."""
    
    def __init__(self):
        """Initialize Google Video Intelligence client."""
        try:
            self.client = videointelligence.VideoIntelligenceServiceClient()
            logger.info("Google Video Intelligence service initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Video Intelligence client: {str(e)}")
            logger.error("Make sure GOOGLE_APPLICATION_CREDENTIALS is set correctly")
            raise
    
    async def analyze_video_explicit_content(self, video_uri: str) -> Dict:
        """
        Analyze video for explicit/adult content detection.
        
        Note: This is a long-running operation that can take several minutes.
        Best used for pre-processing or background tasks, not real-time filtering.
        
        Args:
            video_uri: Google Cloud Storage URI (gs://bucket/video.mp4) or HTTP(S) URL
            
        Returns:
            dict: Analysis results with explicit content annotations including:
                - allowed (bool): Whether video is safe
                - safe (bool): Same as allowed
                - unsafe_frame_count (int): Number of flagged frames
                - unsafe_frames (list): List of unsafe frame timestamps
                - video_uri (str): Original video URI
        """
        try:
            logger.info(f"Starting video analysis for: {video_uri}")
            logger.warning("Video analysis can take 1-5 minutes depending on video length")
            
            # Configure the request for explicit content detection
            features = [videointelligence.Feature.EXPLICIT_CONTENT_DETECTION]
            
            # Start the async operation
            operation = self.client.annotate_video(
                request={
                    "input_uri": video_uri,
                    "features": features,
                }
            )
            
            logger.info("Video processing started... waiting for results")
            
            # Wait for operation to complete (timeout: 10 minutes)
            result = operation.result(timeout=600)
            
            # Process results
            explicit_annotation = result.annotation_results[0].explicit_annotation
            
            # Analyze frames for pornography likelihood
            unsafe_frames = []
            for frame in explicit_annotation.frames:
                # Flag frames with POSSIBLE or higher likelihood
                if frame.pornography_likelihood >= videointelligence.Likelihood.POSSIBLE:
                    unsafe_frames.append({
                        "time_offset_seconds": frame.time_offset.seconds,
                        "likelihood": frame.pornography_likelihood.name
                    })
            
            is_safe = len(unsafe_frames) == 0
            
            result_dict = {
                "allowed": is_safe,
                "safe": is_safe,
                "unsafe_frame_count": len(unsafe_frames),
                "unsafe_frames": unsafe_frames[:20],  # Return first 20 unsafe frames
                "video_uri": video_uri,
                "service": "google_cloud_video_intelligence"
            }
            
            logger.info(
                f"Video analysis complete: Safe={is_safe}, "
                f"Unsafe frames={len(unsafe_frames)}/{len(explicit_annotation.frames)}"
            )
            return result_dict
            
        except Exception as e:
            logger.error(f"Error analyzing video {video_uri}: {str(e)}")
            raise
    
    async def analyze_video_labels(self, video_uri: str) -> Dict:
        """
        Detect labels/objects in video to understand content context.
        
        This can help identify violent content, weapons, etc.
        
        Args:
            video_uri: Google Cloud Storage URI or HTTP(S) URL
            
        Returns:
            dict: Detected labels and their confidence scores
        """
        try:
            logger.info(f"Starting label detection for: {video_uri}")
            
            features = [videointelligence.Feature.LABEL_DETECTION]
            
            operation = self.client.annotate_video(
                request={
                    "input_uri": video_uri,
                    "features": features,
                }
            )
            
            logger.info("Label detection started... waiting for results")
            result = operation.result(timeout=600)
            
            # Extract labels
            labels = []
            for annotation in result.annotation_results[0].segment_label_annotations:
                if annotation.segments:
                    labels.append({
                        "description": annotation.entity.description,
                        "confidence": annotation.segments[0].confidence,
                        "category": annotation.category_entities[0].description if annotation.category_entities else "Unknown"
                    })
            
            # Sort by confidence
            labels.sort(key=lambda x: x["confidence"], reverse=True)
            
            logger.info(f"Detected {len(labels)} labels in video")
            
            # Check for concerning labels
            concerning_labels = ["violence", "weapon", "blood", "fight", "gun", "knife"]
            flagged_labels = [
                label for label in labels 
                if any(concern in label["description"].lower() for concern in concerning_labels)
            ]
            
            return {
                "labels": labels[:30],  # Top 30 labels
                "flagged_labels": flagged_labels,
                "is_concerning": len(flagged_labels) > 0,
                "video_uri": video_uri,
                "service": "google_cloud_video_intelligence"
            }
            
        except Exception as e:
            logger.error(f"Error detecting video labels for {video_uri}: {str(e)}")
            raise
    
    async def quick_video_check(self, video_uri: str) -> bool:
        """
        Quick video safety check combining explicit content and label detection.
        
        Args:
            video_uri: Video URI to check
            
        Returns:
            bool: True if safe, False if unsafe
        """
        try:
            # Run explicit content detection
            explicit_result = await self.analyze_video_explicit_content(video_uri)
            
            # If explicit content found, immediately return unsafe
            if not explicit_result["safe"]:
                logger.warning(f"Video flagged as unsafe: explicit content detected")
                return False
            
            # Check labels for violent/concerning content
            label_result = await self.analyze_video_labels(video_uri)
            
            if label_result["is_concerning"]:
                logger.warning(f"Video flagged as unsafe: concerning labels detected")
                return False
            
            logger.info("Video passed all safety checks")
            return True
            
        except Exception as e:
            logger.error(f"Error in quick video check: {str(e)}")
            # Fail-safe: return False on error
            return False


# Singleton instance
google_video_service = None


def get_video_service() -> GoogleVideoService:
    """
    Get or create GoogleVideoService singleton instance.
    
    Returns:
        GoogleVideoService: Initialized service instance
    """
    global google_video_service
    if google_video_service is None:
        google_video_service = GoogleVideoService()
    return google_video_service
