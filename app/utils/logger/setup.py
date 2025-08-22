from loguru import logger
from .logger_config import LoggerConfig
from .middleware import LoggingMiddleware, PerformanceMiddleware

def setup_logging(settings):
    """Setup production logging configuration"""
    # Initialize logger configuration
    logger_config = LoggerConfig(settings)
    
    # Log startup
    logger.info(
        f"Application starting: {settings.app_name}",
        extra={
            "startup": True,
            "app_name": settings.app_name,
            "app_version": settings.app_version,
            "environment": settings.environment,
            "debug": settings.debug,
        }
    )
    
    return logger

def add_logging_middleware(app, settings):
    """Add logging middleware to FastAPI app"""
    app.add_middleware(LoggingMiddleware, settings=settings)
    app.add_middleware(PerformanceMiddleware, settings=settings)

# Context manager for performance logging
class LogPerformance:
    """Context manager for logging operation performance"""
    
    def __init__(self, operation: str, **kwargs):
        self.operation = operation
        self.kwargs = kwargs
        self.start_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        logger.debug(f"Starting operation: {self.operation}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = time.time() - (self.start_time or time.time())
        
        if exc_type:
            logger.error(
                f"Operation failed: {self.operation}",
                extra={
                    "performance": True,
                    "operation": self.operation,
                    "duration": duration,
                    "error": True,
                    "error_type": exc_type.__name__ if exc_type else None,
                    **self.kwargs
                }
            )
        else:
            logger.info(
                f"Operation completed: {self.operation}",
                extra={
                    "performance": True,
                    "operation": self.operation,
                    "duration": duration,
                    **self.kwargs
                }
            )

import time