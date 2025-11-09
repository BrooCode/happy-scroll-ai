"""
Core configuration module for HappyScroll API.
Loads and validates environment variables.
"""
import os
from typing import Literal
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # OpenAI Configuration
    openai_api_key: str
    
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
