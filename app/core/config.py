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
        description="Path to Google Cloud service account JSON key file"
    )
    google_cloud_project: str = Field(
        default="",
        description="Google Cloud project ID"
    )
    safety_threshold: str = Field(
        default="POSSIBLE",
        description="Safety threshold: UNKNOWN, VERY_UNLIKELY, UNLIKELY, POSSIBLE, LIKELY, VERY_LIKELY"
    )
    
    # Gemini AI Configuration
    gemini_api_key: str = Field(
        default="",
        description="Google Gemini AI API key for content analysis"
    )
    
    # YouTube Data API Configuration
    youtube_api_key: str = Field(
        default="",
        description="YouTube Data API key for fetching video metadata and captions"
    )
    
    # Redis Configuration
    redis_url: str = Field(
        default="",
        description="Redis connection URL for caching (e.g., redis://host:port or redis://user:pass@host:port)"
    )
    
    # Application Environment
    app_env: Literal["dev", "prod"] = "dev"
    
    # Server Configuration
    port: int = 8000
    host: str = "0.0.0.0"
    
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


# Singleton instance
settings = Settings()
