"""
Core configuration module for HappyScroll API.
Loads and validates environment variables.
"""
import os
from typing import Literal
from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Google Cloud Configuration
    google_application_credentials: str = Field(
        default="",
        alias="GOOGLE_APPLICATION_CREDENTIALS",
        description="Path to Google Cloud service account JSON key file"
    )
    google_cloud_project: str = Field(
        default="",
        alias="GOOGLE_CLOUD_PROJECT",
        description="Google Cloud project ID"
    )
    google_vision_key: str = Field(
        default="",
        alias="GOOGLE_VISION_KEY",
        description="Google Cloud Vision API key (optional, can use service account)"
    )
    safety_threshold: str = Field(
        default="POSSIBLE",
        alias="SAFETY_THRESHOLD",
        description="Safety threshold: UNKNOWN, VERY_UNLIKELY, UNLIKELY, POSSIBLE, LIKELY, VERY_LIKELY"
    )
    
    # Gemini AI Configuration
    gemini_api_key: str = Field(
        default="",
        alias="GEMINI_API_KEY",
        description="Google Gemini AI API key for content analysis"
    )
    
    # YouTube Data API Configuration
    youtube_api_key: str = Field(
        default="",
        alias="YOUTUBE_API_KEY",
        description="YouTube Data API key for fetching video metadata and captions"
    )
    
    # Redis Configuration
    redis_url: str = Field(
        default="",
        alias="REDIS_URL",
        description="Redis connection URL for caching (e.g., redis://host:port or redis://user:pass@host:port)"
    )
    
    # Application Environment
    app_env: Literal["dev", "prod"] = Field(
        default="dev",
        alias="APP_ENV"
    )
    
    # Server Configuration
    port: int = Field(default=8000, alias="PORT")
    host: str = Field(default="0.0.0.0", alias="HOST")
    
    # CORS Configuration
    allowed_origins: list[str] = [
        "chrome-extension://*",
        "http://localhost:*",
        "https://localhost:*",
    ]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        populate_by_name = True  # Allow using field names or aliases


# Singleton instance
settings = Settings()
