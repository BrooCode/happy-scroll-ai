"""
Logging configuration for HappyScroll API.
Uses loguru for enhanced logging capabilities.
"""
import sys
from loguru import logger
from app.core.config import settings


def setup_logging() -> None:
    """
    Configure logging with appropriate format and level based on environment.
    """
    # Remove default logger
    logger.remove()
    
    # Determine log level based on environment
    log_level = "DEBUG" if settings.app_env == "dev" else "INFO"
    
    # Add console logger with custom format
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=log_level,
        colorize=True,
    )
    
    # Add file logger for production
    if settings.app_env == "prod":
        logger.add(
            "logs/app.log",
            rotation="500 MB",
            retention="10 days",
            level="INFO",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        )
    
    logger.info(f"Logging configured for {settings.app_env} environment")


# Export configured logger
__all__ = ["logger", "setup_logging"]
