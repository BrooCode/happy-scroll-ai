"""
HappyScroll Moderation API - Main Application
FastAPI backend for Chrome extension content moderation.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.logger import logger, setup_logging
from app.routes import moderation, video_analysis, happyscroll_verdict

# Set up logging
setup_logging()

# Create FastAPI application
app = FastAPI(
    title="HappyScroll Moderation API",
    description="AI-powered content moderation API for the HappyScroll Chrome extension",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS middleware for Chrome extension requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",  # Allow all origins (includes Chrome extensions)
        "chrome-extension://*",  # Explicitly allow Chrome extensions
        "http://localhost:*",  # Allow localhost
        "http://127.0.0.1:*",  # Allow 127.0.0.1
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(moderation.router)
app.include_router(video_analysis.router)
app.include_router(happyscroll_verdict.router)


@app.on_event("startup")
async def startup_event():
    """Execute actions on application startup."""
    logger.info("=" * 60)
    logger.info("HappyScroll Moderation API - Starting up")
    logger.info(f"Environment: {settings.app_env}")
    logger.info(f"Host: {settings.host}:{settings.port}")
    logger.info("=" * 60)


@app.on_event("shutdown")
async def shutdown_event():
    """Execute actions on application shutdown."""
    logger.info("HappyScroll Moderation API - Shutting down")


@app.get("/", tags=["root"])
async def root():
    """
    Root endpoint with API information.
    
    Returns:
        Dict with API metadata
    """
    return {
        "name": "HappyScroll Moderation API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "health": "/api/health",
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler for unhandled exceptions.
    
    Args:
        request: The request object
        exc: The exception that was raised
        
    Returns:
        JSONResponse with error details
    """
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) if settings.app_env == "dev" else "An error occurred",
        },
    )


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.app_env == "dev",
    )
