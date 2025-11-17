"""
Google Cloud Vision API service for content moderation.
Replaces OpenAI moderation with Google's SafeSearch detection.
"""

import io
from typing import Dict, Tuple
from app.core.logger import logger
import aiohttp
from PIL import Image

from google.cloud import vision
from google.cloud.vision_v1 import types


class GoogleVisionService:
    """Service for analyzing image content safety using Google Cloud Vision API."""
    
    # SafeSearch likelihood levels mapping
    LIKELIHOOD_LEVELS = {
        vision.Likelihood.UNKNOWN: 0,
        vision.Likelihood.VERY_UNLIKELY: 1,
        vision.Likelihood.UNLIKELY: 2,
        vision.Likelihood.POSSIBLE: 3,
        vision.Likelihood.LIKELY: 4,
        vision.Likelihood.VERY_LIKELY: 5,
    }
    
    def __init__(self, safety_threshold: str = "POSSIBLE"):
        """
        Initialize Google Vision client.
        
        Args:
            safety_threshold: Minimum likelihood level to flag content as unsafe
                             (UNKNOWN, VERY_UNLIKELY, UNLIKELY, POSSIBLE, LIKELY, VERY_LIKELY)
        """
        try:
            self.client = vision.ImageAnnotatorClient()
            self.threshold = getattr(vision.Likelihood, safety_threshold.upper())
            self.threshold_value = self.LIKELIHOOD_LEVELS[self.threshold]
            logger.info(f"Google Vision service initialized with threshold: {safety_threshold}")
        except Exception as e:
            logger.error(f"Failed to initialize Google Vision client: {str(e)}")
            logger.error("Make sure GOOGLE_APPLICATION_CREDENTIALS is set correctly")
            raise
    
    async def download_image(self, image_url: str) -> bytes:
        """
        Download image from URL asynchronously.
        
        Args:
            image_url: URL of the image to download
            
        Returns:
            bytes: Image content as bytes
            
        Raises:
            Exception: If download fails
        """
        try:
            logger.info(f"Downloading image from: {image_url}")
            
            async with aiohttp.ClientSession() as session:
                async with session.get(image_url, timeout=aiohttp.ClientTimeout(total=15)) as response:
                    if response.status != 200:
                        raise Exception(f"Failed to download image: HTTP {response.status}")
                    
                    content = await response.read()
                    logger.info(f"Successfully downloaded image ({len(content)} bytes)")
                    return content
                    
        except aiohttp.ClientError as e:
            logger.error(f"Network error downloading image from {image_url}: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error downloading image from {image_url}: {str(e)}")
            raise
    
    def analyze_image_bytes(self, image_bytes: bytes) -> vision.SafeSearchAnnotation:
        """
        Analyze image bytes using Google Vision SafeSearch.
        
        Args:
            image_bytes: Image content as bytes
            
        Returns:
            SafeSearchAnnotation: Detection results
            
        Raises:
            Exception: If API call fails
        """
        try:
            logger.info(f"Analyzing image with Google Vision API ({len(image_bytes)} bytes)")
            
            image = vision.Image(content=image_bytes)
            response = self.client.safe_search_detection(image=image)
            
            if response.error.message:
                raise Exception(f"Vision API Error: {response.error.message}")
            
            logger.info("SafeSearch analysis completed successfully")
            return response.safe_search_annotation
            
        except Exception as e:
            logger.error(f"Error analyzing image with Vision API: {str(e)}")
            raise
    
    def is_content_safe(
        self, 
        safe_search: vision.SafeSearchAnnotation
    ) -> Tuple[bool, Dict[str, bool], Dict[str, str]]:
        """
        Determine if content is safe based on SafeSearch results.
        
        Args:
            safe_search: SafeSearch annotation from Vision API
            
        Returns:
            Tuple of:
                - bool: True if safe, False if unsafe
                - dict: Categories flagged (violence, adult, etc)
                - dict: Likelihood levels for each category
        """
        # Check each category against threshold
        categories_flagged = {
            "adult": self.LIKELIHOOD_LEVELS[safe_search.adult] >= self.threshold_value,
            "violence": self.LIKELIHOOD_LEVELS[safe_search.violence] >= self.threshold_value,
            "racy": self.LIKELIHOOD_LEVELS[safe_search.racy] >= self.threshold_value,
            "medical": self.LIKELIHOOD_LEVELS[safe_search.medical] >= self.threshold_value,
            "spoof": self.LIKELIHOOD_LEVELS[safe_search.spoof] >= self.threshold_value,
        }
        
        likelihood_scores = {
            "adult": safe_search.adult.name,
            "violence": safe_search.violence.name,
            "racy": safe_search.racy.name,
            "medical": safe_search.medical.name,
            "spoof": safe_search.spoof.name,
        }
        
        # Content is safe if NO categories are flagged
        is_safe = not any(categories_flagged.values())
        
        flagged_list = [cat for cat, flagged in categories_flagged.items() if flagged]
        logger.info(
            f"Content safety: {'SAFE' if is_safe else 'UNSAFE'} | "
            f"Flagged: {flagged_list if flagged_list else 'None'}"
        )
        
        return is_safe, categories_flagged, likelihood_scores
    
    async def is_safe_content(self, image_url: str) -> bool:
        """
        Main function to check if content from URL is safe for kids.
        
        This is the primary function for the HappyScroll extension to use.
        
        Args:
            image_url: URL of the image/thumbnail to check
            
        Returns:
            bool: True if safe for kids, False if should be skipped
        """
        try:
            logger.info(f"Checking content safety for: {image_url}")
            
            # Step 1: Download the image
            image_bytes = await self.download_image(image_url)
            
            # Step 2: Analyze with Vision API
            safe_search = self.analyze_image_bytes(image_bytes)
            
            # Step 3: Check if safe
            is_safe, categories, scores = self.is_content_safe(safe_search)
            
            logger.info(f"Final result for {image_url}: {'SAFE' if is_safe else 'UNSAFE'}")
            return is_safe
            
        except Exception as e:
            logger.error(f"Error checking content safety for {image_url}: {str(e)}")
            # On error, return False (unsafe) to be cautious and skip content
            logger.warning("Returning UNSAFE due to error (fail-safe behavior)")
            return False
    
    async def analyze_content(self, image_url: str) -> Dict:
        """
        Comprehensive content analysis with detailed results.
        
        Args:
            image_url: URL of the image to analyze
            
        Returns:
            dict: Detailed analysis results including:
                - allowed (bool): Whether content is allowed
                - safe (bool): Same as allowed (for compatibility)
                - categories (dict): Which categories were flagged
                - likelihood_scores (dict): Confidence levels for each category
                - threshold (str): Threshold level used
                - image_url (str): Original URL analyzed
        """
        try:
            logger.info(f"Starting comprehensive analysis for: {image_url}")
            
            # Download image
            image_bytes = await self.download_image(image_url)
            
            # Analyze with Vision API
            safe_search = self.analyze_image_bytes(image_bytes)
            
            # Get safety results
            is_safe, categories_flagged, likelihood_scores = self.is_content_safe(safe_search)
            
            result = {
                "allowed": is_safe,
                "safe": is_safe,
                "categories": categories_flagged,
                "likelihood_scores": likelihood_scores,
                "threshold": self.threshold.name,
                "image_url": image_url,
                "service": "google_cloud_vision"
            }
            
            logger.info(f"Analysis complete: allowed={is_safe}, flagged_categories={[k for k, v in categories_flagged.items() if v]}")
            return result
            
        except Exception as e:
            logger.error(f"Error in analyze_content for {image_url}: {str(e)}")
            raise


# Singleton instance
google_vision_service = None


def get_vision_service(safety_threshold: str = "POSSIBLE") -> GoogleVisionService:
    """
    Get or create GoogleVisionService singleton instance.
    
    Args:
        safety_threshold: Safety threshold level
        
    Returns:
        GoogleVisionService: Initialized service instance
    """
    global google_vision_service
    if google_vision_service is None:
        google_vision_service = GoogleVisionService(safety_threshold)
    return google_vision_service
