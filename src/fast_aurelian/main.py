import os
import sys

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger

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


from .api.routes import register_routes


def setup_paperqa_environment(settings):
    """Setup PaperQA environment variables at app startup."""
    from pathlib import Path
    
    # Set default paper directory if not already set
    if not os.environ.get("PQA_HOME"):
        default_paper_dir = Path.cwd() / "papers"
        default_paper_dir.mkdir(exist_ok=True)
        os.environ["PQA_HOME"] = str(default_paper_dir)
        logger.info(f"Set PQA_HOME to: {default_paper_dir}")
    
    # Set Aurelian workdir if specified in settings
    if hasattr(settings, 'aurelian_workdir') and settings.aurelian_workdir:
        workdir_path = Path(settings.aurelian_workdir)
        workdir_path.mkdir(exist_ok=True)
        os.environ["AURELIAN_WORKDIR"] = str(workdir_path)
        # Also set PQA_HOME to the same location
        os.environ["PQA_HOME"] = str(workdir_path)
        logger.info(f"Set AURELIAN_WORKDIR and PQA_HOME to: {workdir_path}")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()
    
    # Setup PaperQA environment at startup
    setup_paperqa_environment(settings)
    
    logger.remove()
    logger.add(
        sys.stderr, format=settings.log_format, level=settings.log_level.upper(), colorize=True
    )

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        docs_url=settings.docs_url,
        redoc_url=settings.redoc_url,
        debug=settings.debug,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=settings.cors_methods,
        allow_headers=settings.cors_headers,
    )

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
                },
            },
        )

    if has_config:
        app.middleware("http")(logging_middleware)

    register_routes(app)

    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        return {"status": "healthy", "service": settings.app_name}

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


app = create_app()

if __name__ == "__main__":
    import uvicorn

    host = os.environ.get("FAST_AURELIAN_HOST", "127.0.0.1")
    port = int(os.environ.get("FAST_AURELIAN_PORT", 8000))
    logger.info(f"Starting {app.title} on {host}:{port}")
    uvicorn.run("fast_aurelian.main:app", host=host, port=port, reload=True)
