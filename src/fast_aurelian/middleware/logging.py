import time
import uuid
from collections.abc import Callable

from fastapi import Request, Response
from loguru import logger


async def logging_middleware(request: Request, call_next: Callable) -> Response:
    """
    Middleware for logging requests and responses with correlation IDs.

    Args:
        request: The incoming request
        call_next: The next middleware/endpoint handler

    Returns:
        The response with correlation ID header
    """
    correlation_id = str(uuid.uuid4())
    request.state.correlation_id = correlation_id
    start_time = time.time()
    logger.info(
        "Request started",
        extra={
            "correlation_id": correlation_id,
            "method": request.method,
            "url": str(request.url),
            "user_agent": request.headers.get("user-agent"),
            "client_ip": request.client.host if request.client else None,
        },
    )

    try:
        response = await call_next(request)
        duration = time.time() - start_time
        logger.info(
            "Request completed",
            extra={
                "correlation_id": correlation_id,
                "status_code": response.status_code,
                "duration_ms": round(duration * 1000, 2),
            },
        )
        response.headers["X-Correlation-ID"] = correlation_id
        return response

    except Exception as e:
        duration = time.time() - start_time
        logger.error(
            "Request failed",
            extra={
                "correlation_id": correlation_id,
                "error": str(e),
                "duration_ms": round(duration * 1000, 2),
            },
        )
        raise
