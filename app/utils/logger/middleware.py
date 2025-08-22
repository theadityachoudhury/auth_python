import time
import traceback
import uuid
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from loguru import logger
from .logger_config import LoggerUtils

class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for comprehensive request/response logging"""
    
    def __init__(self, app, settings):
        super().__init__(app)
        self.settings = settings
        self.excluded_paths = ["/health", "/metrics", "/favicon.ico"]
        self.sensitive_headers = ["authorization", "cookie", "x-api-key"]
    
    async def dispatch(self, request: Request, call_next):
        # Skip logging for excluded paths
        if request.url.path in self.excluded_paths:
            return await call_next(request)
        
        request_id = str(uuid.uuid4())
        LoggerUtils.set_request_context(request_id)
        
        # Capture request body for POST/PUT requests
        request_body = None
        if request.method in ["POST", "PUT", "PATCH"]:
            try:
                body = await request.body()
                if body:
                    # Don't log sensitive data
                    if "password" not in str(body).lower():
                        request_body = body.decode("utf-8")[:1000]  # Limit size
            except:
                pass
        
        # Log request with rich context
        logger.info("Request received", extra={
            "request": True,
            "request_id": request_id,
            "method": request.method,
            "url": str(request.url),
            "path": request.url.path,
            "query_params": dict(request.query_params),
            "headers": self._filter_sensitive_headers(dict(request.headers)),
            "client_ip": self._get_client_ip(request),
            "user_agent": request.headers.get("user-agent", ""),
            "content_type": request.headers.get("content-type", ""),
            "content_length": request.headers.get("content-length", 0),
            "request_body": request_body,
            "referer": request.headers.get("referer"),
            "accept": request.headers.get("accept"),
            "accept_encoding": request.headers.get("accept-encoding"),
            "accept_language": request.headers.get("accept-language")
        })
        
        start_time = time.time()
        
        # Process request
        try:
            response = await call_next(request)
            duration = time.time() - start_time
            
            # Capture response details
            response_headers = dict(response.headers)
            
            # Log response
            logger.info("Request completed", extra={
                "request": True,
                "response": True,
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration": duration,
                "response_headers": response_headers,
                "content_type": response.headers.get("content-type", ""),
                "content_length": response.headers.get("content-length", 0),
                "cache_control": response.headers.get("cache-control"),
                "server_timing": f"total;dur={duration*1000:.2f}"
            })
            
            # Add performance headers
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Response-Time"] = f"{duration*1000:.2f}ms"
            
            # Log performance warnings
            if duration > 2.0:
                logger.warning("Slow request detected", extra={
                    "performance": True,
                    "slow_request": True,
                    "request_id": request_id,
                    "path": request.url.path,
                    "duration": duration,
                    "threshold_exceeded": "2s"
                })
            
            return response
            
        except Exception as e:
            duration = time.time() - start_time
            
            logger.error("Request failed", extra={
                "request": True,
                "error": True,
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "duration": duration,
                "error_type": type(e).__name__,
                "error_message": str(e),
                "traceback": traceback.format_exc()
            })
            
            raise
        
        finally:
            LoggerUtils.clear_request_context()
    
    def _filter_sensitive_headers(self, headers: dict) -> dict:
        """Filter out sensitive headers"""
        filtered = {}
        for key, value in headers.items():
            if key.lower() in self.sensitive_headers:
                filtered[key] = "[REDACTED]"
            else:
                filtered[key] = value
        return filtered
    
    def _get_client_ip(self, request: Request) -> str:
        """Get real client IP"""
        # Check various headers in order of preference
        ip_headers = [
            "X-Forwarded-For",
            "X-Real-IP",
            "X-Client-IP",
            "CF-Connecting-IP",  # Cloudflare
            "True-Client-IP"     # Akamai
        ]
        
        for header in ip_headers:
            if header in request.headers:
                ip = request.headers[header].split(",")[0].strip()
                if ip:
                    return ip
        
        return request.client.host if request.client else "unknown"
    
class PerformanceMiddleware(BaseHTTPMiddleware):
    """Middleware for performance monitoring"""
    
    def __init__(self, app, settings):
        super().__init__(app)
        self.settings = settings
        self.slow_threshold = 1.0  # seconds
        self.very_slow_threshold = 5.0  # seconds
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        
        response = await call_next(request)
        
        duration = time.time() - start_time
        
        # Log performance metrics
        if duration > self.very_slow_threshold:
            logger.warning(
                f"Very slow request: {request.method} {request.url.path}",
                extra={
                    "performance": True,
                    "very_slow": True,
                    "method": request.method,
                    "path": request.url.path,
                    "duration": duration,
                    "threshold": self.very_slow_threshold,
                }
            )
        elif duration > self.slow_threshold:
            logger.info(
                f"Slow request: {request.method} {request.url.path}",
                extra={
                    "performance": True,
                    "slow": True,
                    "method": request.method,
                    "path": request.url.path,
                    "duration": duration,
                    "threshold": self.slow_threshold,
                }
            )
        
        return response