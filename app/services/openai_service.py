"""
OpenAI service for content moderation.
Handles all interactions with OpenAI's moderation API.
"""
import time
from typing import Dict, List, Tuple
from openai import OpenAI, OpenAIError, BadRequestError, RateLimitError
from app.core.config import settings
from app.core.logger import logger


class OpenAIService:
    """Service class for OpenAI moderation API interactions."""
    
    def __init__(self):
        """Initialize OpenAI client with API key from settings."""
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.primary_model = "omni-moderation-latest"
        self.fallback_model = "text-moderation-latest"
        self.max_retries = 3
        self.retry_delay = 2  # seconds
        logger.info("OpenAI service initialized")
    
    async def moderate_content(self, content: str) -> Tuple[bool, List[str], Dict[str, float]]:
        """
        Moderate content using OpenAI's moderation API.
        
        Args:
            content: The text content to moderate
            
        Returns:
            Tuple containing:
                - safe (bool): True if content is safe, False if flagged
                - categories (List[str]): List of flagged category names
                - category_scores (Dict[str, float]): Scores for each category
                
        Raises:
            OpenAIError: If the API call fails
            Exception: For other unexpected errors
        """
        try:
            logger.info(f"Moderating content (length: {len(content)} chars)")
            
            # Try primary model first (omni-moderation-latest) with retry logic
            response = self._call_moderation_api_with_retry(content, self.primary_model)
            
        except RateLimitError as e:
            # Handle 429 rate limit errors specifically
            logger.error(f"Rate limit exceeded: {str(e)}")
            logger.warning(
                "Rate limit hit. Please check your OpenAI account: "
                "https://platform.openai.com/account/usage"
            )
            raise OpenAIError(
                "Rate limit exceeded. Please wait a moment and try again. "
                "If this persists, check your OpenAI account billing and usage limits."
            )
        except BadRequestError as e:
            # Check if error is related to invalid model name
            error_message = str(e).lower()
            if "model" in error_message or "invalid" in error_message:
                logger.warning(
                    f"Primary model '{self.primary_model}' failed, "
                    f"retrying with fallback model '{self.fallback_model}': {str(e)}"
                )
                try:
                    # Retry with fallback model
                    response = self._call_moderation_api(content, self.fallback_model)
                except Exception as fallback_error:
                    logger.error(f"Fallback model also failed: {str(fallback_error)}")
                    raise
            else:
                logger.error(f"OpenAI BadRequest error: {str(e)}")
                raise
        except OpenAIError as e:
            logger.error(f"OpenAI API error during moderation: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during moderation: {str(e)}")
            raise
        
        # Process the response
        try:
            # Extract results from the first result object
            result = response.results[0]
            
            # Determine if content is safe (not flagged)
            safe = not result.flagged
            
            # Extract flagged categories
            flagged_categories = []
            category_scores = {}
            
            # Process all categories
            if hasattr(result, 'categories') and hasattr(result, 'category_scores'):
                categories_dict = result.categories.model_dump()
                scores_dict = result.category_scores.model_dump()
                
                for category, is_flagged in categories_dict.items():
                    score = scores_dict.get(category, 0.0)
                    category_scores[category] = score
                    
                    if is_flagged:
                        flagged_categories.append(category)
            
            logger.info(
                f"Moderation complete - Safe: {safe}, "
                f"Flagged categories: {flagged_categories if flagged_categories else 'None'}"
            )
            
            return safe, flagged_categories, category_scores
            
        except Exception as e:
            logger.error(f"Error processing moderation response: {str(e)}")
            raise
    
    def _call_moderation_api(self, content: str, model: str):
        """
        Internal method to call OpenAI moderation API with specified model.
        
        Args:
            content: The text content to moderate
            model: The model name to use
            
        Returns:
            OpenAI moderation response
        """
        logger.debug(f"Calling moderation API with model: {model}")
        return self.client.moderations.create(
            model=model,
            input=content
        )
    
    def _call_moderation_api_with_retry(self, content: str, model: str, retry_count: int = 0):
        """
        Call moderation API with exponential backoff retry logic for rate limits.
        
        Args:
            content: The text content to moderate
            model: The model name to use
            retry_count: Current retry attempt number
            
        Returns:
            OpenAI moderation response
            
        Raises:
            RateLimitError: If rate limit persists after retries
        """
        try:
            return self._call_moderation_api(content, model)
        except RateLimitError as e:
            if retry_count < self.max_retries:
                wait_time = self.retry_delay * (2 ** retry_count)  # Exponential backoff
                logger.warning(
                    f"Rate limit hit (attempt {retry_count + 1}/{self.max_retries}). "
                    f"Waiting {wait_time} seconds before retry..."
                )
                time.sleep(wait_time)
                return self._call_moderation_api_with_retry(content, model, retry_count + 1)
            else:
                logger.error(f"Rate limit exceeded after {self.max_retries} retries")
                raise


# Singleton instance
openai_service = OpenAIService()
