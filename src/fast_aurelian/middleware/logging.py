import time
import uuid
from typing import Callable
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
    # Generate correlation ID
    correlation_id = str(uuid.uuid4())
    
    # Add correlation ID to request state
    request.state.correlation_id = correlation_id
    
    # Start timing
    start_time = time.time()
    
    # Log incoming request
    logger.info(
        f"Request started",
        extra={
            "correlation_id": correlation_id,
            "method": request.method,
            "url": str(request.url),
            "user_agent": request.headers.get("user-agent"),
            "client_ip": request.client.host if request.client else None,
        }
    )
    
    try:
        # Process request
        response = await call_next(request)
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Log response
        logger.info(
            f"Request completed",
            extra={
                "correlation_id": correlation_id,
                "status_code": response.status_code,
                "duration_ms": round(duration * 1000, 2),
            }
        )
        
        # Add correlation ID to response headers
        response.headers["X-Correlation-ID"] = correlation_id
        
        return response
        
    except Exception as e:
        # Calculate duration for failed requests
        duration = time.time() - start_time
        
        # Log error
        logger.error(
            f"Request failed",
            extra={
                "correlation_id": correlation_id,
                "error": str(e),
                "duration_ms": round(duration * 1000, 2),
            }
        )
        
        # Re-raise the exception
        raise