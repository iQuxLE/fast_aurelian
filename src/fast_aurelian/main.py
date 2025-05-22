from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
import sys
import os

# Use a try/except here since config.py might not exist yet in this implementation
try:
    from .config import Settings, get_settings
    from .middleware.logging import logging_middleware
    has_config = True
except ImportError:
    has_config = False
    # Fallback default settings
    class Settings:
        app_name = "Fast-Aurelian"
        app_version = "0.1.0"
        docs_url = "/docs"
        redoc_url = "/redoc"
        debug = True
        cors_origins = ["*"]
        cors_methods = ["*"]
        cors_headers = ["*"]
        log_format = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
        log_level = "INFO"
        
    def get_settings():
        return Settings()

# Import API routes
from .api import paperqa
from .api.routes import register_routes


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()
    
    # Configure loguru
    logger.remove()  # Remove default handler
    logger.add(
        sys.stderr,
        format=settings.log_format,
        level=settings.log_level.upper(),
        colorize=True
    )
    
    # Create FastAPI app
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        docs_url=settings.docs_url,
        redoc_url=settings.redoc_url,
        debug=settings.debug,
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=settings.cors_methods,
        allow_headers=settings.cors_headers,
    )
    
    # Add exception handler for clean error responses
    @app.exception_handler(Exception)
    async def generic_exception_handler(request, exc):
        """Handle all exceptions with a clean JSON response."""
        status_code = 500
        
        if isinstance(exc, HTTPException):
            status_code = exc.status_code
        
        return JSONResponse(
            status_code=status_code,
            content={
                "status": "error",
                "error": {
                    "message": str(exc),
                    "type": type(exc).__name__,
                }
            },
        )
    
    # Add logging middleware if available
    if has_config:
        app.middleware("http")(logging_middleware)
    
    # Register API routes
    register_routes(app)
    
    # Health check endpoint
    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        return {"status": "healthy", "service": settings.app_name}
    
    # Root endpoint
    @app.get("/")
    async def root():
        """Root endpoint with basic info."""
        return {
            "service": settings.app_name,
            "version": settings.app_version,
            "docs": settings.docs_url,
            "redoc": settings.redoc_url,
            "agents": ["paperqa"],
        }
    
    return app


# Create the app instance
app = create_app()

# Run the application with Uvicorn if executed directly
if __name__ == "__main__":
    import uvicorn
    
    host = os.environ.get("FAST_AURELIAN_HOST", "127.0.0.1")
    port = int(os.environ.get("FAST_AURELIAN_PORT", 8000))
    
    logger.info(f"Starting {app.title} on {host}:{port}")
    uvicorn.run("fast_aurelian.main:app", host=host, port=port, reload=True)