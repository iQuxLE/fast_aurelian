"""
Routes registration for Fast-Aurelian.
"""

from fastapi import FastAPI

from . import paperqa


def register_routes(app: FastAPI) -> None:
    """
    Register all API routes with the FastAPI application.

    Args:
        app: FastAPI application instance
    """
    app.include_router(paperqa.router)
