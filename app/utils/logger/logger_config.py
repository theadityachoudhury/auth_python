import sys
import json
import time
from pathlib import Path
from typing import Dict, Any, Optional
from loguru import logger
from contextvars import ContextVar
import traceback
from typing import Union, Callable

# Context variables for request tracking
request_id_var: ContextVar[Optional[str]] = ContextVar('request_id', default=None)
user_id_var: ContextVar[Optional[str]] = ContextVar('user_id', default=None)

class CustomFormatter:
    """Custom formatter for structured logging"""
    
    def __init__(self, settings, include_extra: bool = True):
        self.settings = settings
        self.include_extra = include_extra
    
    def format(self, record)->str:
        """Format log record with additional context"""
        # Get context variables
        request_id = request_id_var.get()
        user_id = user_id_var.get()
        
        # Base log data
        log_data = {
            "timestamp": record["time"].isoformat(),
            "level": record["level"].name,
            "logger": record["name"],
            "message": record["message"],
            "module": record["module"],
            "function": record["function"],
            "line": record["line"],
            "process_id": record["process"].id,
            "thread_id": record["thread"].id,
            "environment": self.settings.environment,
            "app_name": self.settings.app_name,
            "app_version": self.settings.app_version,
        }
        
        # Add context if available
        if request_id:
            log_data["request_id"] = request_id
        if user_id:
            log_data["user_id"] = user_id
            
        # Add exception info if present
        if record["exception"]:
            log_data["exception"] = {
                "type": record["exception"].type.__name__,
                "value": str(record["exception"].value),
                "traceback": traceback.format_exception(
                    record["exception"].type,
                    record["exception"].value,
                    record["exception"].traceback
                )
            }
        
        # Add extra fields
        if self.include_extra and record["extra"]:
            log_data["extra"] = record["extra"]
            
        return json.dumps(log_data, ensure_ascii=False)

class LoggerConfig:
    """Production-grade logger configuration"""
    
    def __init__(self, settings):
        self.settings = settings
        self._setup_logger()
    
    def _setup_logger(self):
        """Setup loguru logger with production configurations"""
        # Remove default logger
        logger.remove()
        
        # Setup console logging
        if self.settings.log_console:
            if self.settings.log_json:
                # For JSON console output, use serialize=True and no color
                logger.add(
                    sys.stdout,
                    level=self.settings.log_level,
                    backtrace=self.settings.log_backtrace,
                    diagnose=self.settings.debug,
                    enqueue=True,  # Thread-safe logging
                    catch=True,    # Catch exceptions in logging
                    serialize=True,  # JSON format
                )
            else:
                console_format = self._get_console_format()
                logger.add(
                    sys.stdout,
                    format=console_format,
                    level=self.settings.log_level,
                    colorize=self.settings.log_color,
                    backtrace=self.settings.log_backtrace,
                    diagnose=self.settings.debug,
                    enqueue=True,  # Thread-safe logging
                    catch=True,    # Catch exceptions in logging
                )
        
        # Setup file logging
        if self.settings.log_file:
            self._setup_file_logging()
        
        # Setup exception logging
        if self.settings.log_exception:
            self._setup_exception_logging()
            
        # Setup request logging
        self._setup_request_logger()
    

    def _get_console_format(self) -> str:
        """Get console format based on settings"""
        if self.settings.log_color:
            return (
                "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
                "<level>{level: <8}</level> | "
                "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
                "<level>{message}</level>"
            )
        else:
            # Use loguru format syntax instead of Python % formatting
            return "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} | {message}"
    
    def _setup_file_logging(self):
        """Setup file logging with rotation"""
        # Ensure log directory exists
        log_path = Path(self.settings.log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        if self.settings.log_json:
            # For JSON logging, we'll use serialize=True instead of custom formatter
            logger.add(
                self.settings.log_file,
                level=self.settings.log_level,
                rotation=self._parse_rotation(self.settings.log_rotation),
                retention=self._parse_retention(self.settings.log_retention),
                compression="gz" if self.settings.log_compression else None,
                backtrace=self.settings.log_backtrace,
                diagnose=self.settings.debug,
                enqueue=True,
                catch=True,
                serialize=True,  # This will output JSON format
            )
        else:
            # Use loguru's format string syntax for regular text format
            file_format = "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} | {message}"
            logger.add(
                self.settings.log_file,
                format=file_format,
                level=self.settings.log_level,
                rotation=self._parse_rotation(self.settings.log_rotation),
                retention=self._parse_retention(self.settings.log_retention),
                compression="gz" if self.settings.log_compression else None,
                backtrace=self.settings.log_backtrace,
                diagnose=self.settings.debug,
                enqueue=True,
                catch=True,
                serialize=False,
            )
    
    def _setup_exception_logging(self):
        """Setup separate exception logging"""
        # Ensure exception log directory exists
        exception_path = Path(self.settings.log_exception_file)
        exception_path.parent.mkdir(parents=True, exist_ok=True)
        
        if self.settings.log_exception_json:
            # For JSON logging, use serialize=True
            logger.add(
                self.settings.log_exception_file,
                level=self.settings.log_exception_level,
                rotation=self._parse_rotation(self.settings.log_exception_rotation),
                retention=self._parse_retention(self.settings.log_exception_retention),
                compression="gz" if self.settings.log_exception_compression else None,
                backtrace=self.settings.log_exception_backtrace,
                diagnose=self.settings.debug,
                enqueue=True,
                catch=True,
                serialize=True,  # JSON format
                filter=lambda record: record["level"].no >= logger.level(self.settings.log_exception_level).no
            )
        else:
            # Use loguru's format string syntax for exceptions with more detail
            exception_format = "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} | {message}"
            logger.add(
                self.settings.log_exception_file,
                format=exception_format,
                level=self.settings.log_exception_level,
                rotation=self._parse_rotation(self.settings.log_exception_rotation),
                retention=self._parse_retention(self.settings.log_exception_retention),
                compression="gz" if self.settings.log_exception_compression else None,
                backtrace=self.settings.log_exception_backtrace,
                diagnose=self.settings.debug,
                enqueue=True,
                catch=True,
                serialize=False,
                filter=lambda record: record["level"].no >= logger.level(self.settings.log_exception_level).no
            )
    
    def _setup_request_logger(self):
        """Setup separate request logger"""
        request_log_file = "logs/requests.log"
        Path(request_log_file).parent.mkdir(parents=True, exist_ok=True)
        
        # Fixed filter function - loguru wraps extra data in another 'extra' key
        def request_filter(record):
            extra = record.get("extra", {})
            # Loguru wraps the extra data in another "extra" key
            actual_extra = extra.get("extra", {})
            return "request" in actual_extra
        
        if self.settings.log_json:
            # For JSON logging, use serialize=True
            logger.add(
                request_log_file,
                level="INFO",
                rotation="1 day",
                retention="30 days",
                compression="gz",
                enqueue=True,
                catch=True,
                serialize=True,  # JSON format
                filter=request_filter
            )
        else:
            # Use loguru's format string syntax for requests
            request_format = "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | REQUEST | {message}"
            logger.add(
                request_log_file,
                format=request_format,
                level="INFO",
                rotation="1 day",
                retention="30 days",
                compression="gz",
                enqueue=True,
                catch=True,
                serialize=False,
                filter=request_filter
            )
    
    def _parse_rotation(self, rotation: str):
        """Parse rotation string to loguru format"""
        if rotation.endswith(" day") or rotation.endswith(" days"):
            return rotation
        elif rotation.endswith("MB"):
            return f"{rotation.replace('MB', '')} MB"
        elif rotation.endswith("GB"):
            return f"{rotation.replace('GB', '')} GB"
        return rotation
    
    def _parse_retention(self, retention: str):
        """Parse retention string to loguru format"""
        if retention.endswith(" day") or retention.endswith(" days"):
            return retention
        return retention

# Logger utilities
class LoggerUtils:
    """Utility functions for logging"""
    
    @staticmethod
    def set_request_context(request_id: str, user_id: Optional[str] = None):
        """Set request context for logging"""
        request_id_var.set(request_id)
        if user_id:
            user_id_var.set(user_id)
    
    @staticmethod
    def clear_request_context():
        """Clear request context"""
        request_id_var.set(None)
        user_id_var.set(None)
    
    @staticmethod
    def log_performance(operation: str, duration: float, **kwargs):
        """Log performance metrics"""
        logger.info(
            f"Performance: {operation} completed in {duration:.4f}s",
            extra={
                "performance": True,
                "operation": operation,
                "duration": duration,
                **kwargs
            }
        )
    
    @staticmethod
    def log_business_event(event: str, **kwargs):
        """Log business events"""
        logger.info(
            f"Business Event: {event}",
            extra={
                "business_event": True,
                "event": event,
                **kwargs
            }
        )
    
    @staticmethod
    def log_security_event(event: str, severity: str = "INFO", **kwargs):
        """Log security events"""
        log_func = getattr(logger, severity.lower(), logger.info)
        log_func(
            f"Security Event: {event}",
            extra={
                "security_event": True,
                "event": event,
                "severity": severity,
                **kwargs
            }
        )