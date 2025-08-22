# Logger Documentation

## Overview

This project uses a comprehensive logging system built on top of [Loguru](https://loguru.readthedocs.io/), providing production-grade logging capabilities with structured JSON output, performance monitoring, request tracking, and extensive configuration options.

## Features

### 🚀 **Core Features**
- **Structured JSON Logging**: Machine-readable logs with rich metadata
- **Request Tracking**: Automatic request ID generation and context tracking  
- **Performance Monitoring**: Built-in performance metrics and slow request detection
- **Security Logging**: Specialized security event logging with sensitive data filtering
- **Multiple Output Formats**: Support for both human-readable and JSON formats
- **File Rotation & Compression**: Automatic log rotation with compression support
- **Thread-Safe**: Enqueued logging for high-concurrency applications
- **Exception Handling**: Dedicated exception logging with full stack traces

### 🔧 **Advanced Features**
- **Context Variables**: Request ID and user ID tracking across async operations
- **Custom Formatters**: Rich log formatting with application metadata
- **Middleware Integration**: Automatic HTTP request/response logging
- **Business Event Logging**: Specialized logging for business logic events
- **Performance Context Manager**: Easy performance measurement for operations
- **Sensitive Data Filtering**: Automatic redaction of sensitive headers and data

## Quick Start

### 1. Basic Setup

```python
from app.utils.logger.setup import setup_logging
from app.config.settings import settings

# Initialize logging
logger = setup_logging(settings)

# Basic logging
logger.info("Application started")
logger.warning("This is a warning")
logger.error("This is an error")
```

### 2. FastAPI Integration

```python
from fastapi import FastAPI
from app.utils.logger.setup import setup_logging, add_logging_middleware
from app.config.settings import settings

app = FastAPI()

# Setup logging
logger = setup_logging(settings)

# Add logging middleware
add_logging_middleware(app, settings)
```

## Configuration

### Environment Variables

Configure logging behavior using environment variables or the settings file:

| Variable | Default | Description |
|----------|---------|-------------|
| `LOG_LEVEL` | `"INFO"` | Minimum log level (DEBUG, INFO, WARNING, ERROR, CRITICAL) |
| `LOG_FORMAT` | Custom format | Log format string for non-JSON output |
| `LOG_FILE` | `"app.log"` | Main log file path |
| `LOG_ROTATION` | `"1 day"` | Log rotation interval (e.g., "1 day", "100 MB") |
| `LOG_RETENTION` | `"7 days"` | Log retention period |
| `LOG_COMPRESSION` | `true` | Enable gzip compression for rotated logs |
| `LOG_JSON` | `false` | Enable structured JSON logging |
| `LOG_CONSOLE` | `true` | Enable console output |
| `LOG_COLOR` | `true` | Enable colored console output |
| `LOG_BACKTRACE` | `false` | Include backtrace in logs |

### Exception Logging Configuration

Separate configuration for exception logs:

| Variable | Default | Description |
|----------|---------|-------------|
| `LOG_EXCEPTION` | `true` | Enable separate exception logging |
| `LOG_EXCEPTION_FILE` | `"exception.log"` | Exception log file path |
| `LOG_EXCEPTION_LEVEL` | `"ERROR"` | Minimum level for exception logs |
| `LOG_EXCEPTION_JSON` | `false` | JSON format for exception logs |
| `LOG_EXCEPTION_ROTATION` | `"1 day"` | Exception log rotation |
| `LOG_EXCEPTION_RETENTION` | `"7 days"` | Exception log retention |

### Example Configuration

```python
# settings.py
class Settings:
    # Basic logging
    log_level: str = "INFO"
    log_json: bool = True  # Enable JSON logging
    log_file: str = "logs/app.log"
    log_rotation: str = "100 MB"
    log_retention: str = "30 days"
    log_compression: bool = True
    
    # Exception logging
    log_exception: bool = True
    log_exception_file: str = "logs/exceptions.log"
    log_exception_level: str = "ERROR"
```

## Usage Examples

### Basic Logging

```python
from loguru import logger

# Simple logging
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical message")

# Logging with extra context
logger.info("User logged in", extra={
    "user_id": "12345",
    "action": "login",
    "ip_address": "192.168.1.100"
})
```

### Request Context Tracking

```python
from app.utils.logger.logger_config import LoggerUtils
from loguru import logger

# Set request context
LoggerUtils.set_request_context(request_id="req-12345", user_id="user-67890")

# All subsequent logs will include request_id and user_id
logger.info("Processing user request")

# Clear context when done
LoggerUtils.clear_request_context()
```

### Performance Logging

#### Using Utility Methods

```python
from app.utils.logger.logger_config import LoggerUtils
import time

start_time = time.time()
# ... perform operation ...
duration = time.time() - start_time

# Log performance
LoggerUtils.log_performance("database_query", duration, query="SELECT * FROM users")
```

#### Using Context Manager

```python
from app.utils.logger.setup import LogPerformance

# Automatic performance logging
with LogPerformance("expensive_operation", operation_type="calculation"):
    # Your expensive operation here
    result = complex_calculation()
```

### Business Event Logging

```python
from app.utils.logger.logger_config import LoggerUtils

# Log business events
LoggerUtils.log_business_event("user_registration", 
    user_id="12345",
    email="user@example.com",
    plan="premium"
)

LoggerUtils.log_business_event("payment_processed",
    user_id="12345", 
    amount=99.99,
    currency="USD",
    payment_method="credit_card"
)
```

### Security Event Logging

```python
from app.utils.logger.logger_config import LoggerUtils

# Log security events
LoggerUtils.log_security_event("failed_login_attempt",
    severity="WARNING",
    user_id="12345",
    ip_address="192.168.1.100",
    attempts_count=3
)

LoggerUtils.log_security_event("suspicious_activity",
    severity="ERROR",
    user_id="12345",
    activity_type="rapid_api_calls",
    request_count=1000,
    time_window="1 minute"
)
```

### Exception Logging

```python
from loguru import logger

try:
    # Some operation that might fail
    risky_operation()
except Exception as e:
    # Automatic exception logging with stack trace
    logger.exception("Operation failed")
    
    # Or with additional context
    logger.exception("Database operation failed", extra={
        "operation": "user_update",
        "user_id": "12345",
        "table": "users"
    })
```

## Middleware Features

### Request/Response Logging

The logging middleware automatically captures:

- **Request Details**:
  - HTTP method, URL, path, query parameters
  - Headers (sensitive headers redacted)
  - Client IP, User Agent, Content Type
  - Request body (for POST/PUT, excluding sensitive data)
  - Referer, Accept headers

- **Response Details**:
  - Status code, response headers
  - Content type and length
  - Response time in headers (`X-Response-Time`)
  - Request ID in headers (`X-Request-ID`)

- **Performance Monitoring**:
  - Request duration tracking
  - Slow request warnings (>2 seconds)
  - Very slow request alerts (>5 seconds)

### Sensitive Data Protection

The middleware automatically filters sensitive information:

- **Headers**: `authorization`, `cookie`, `x-api-key` are redacted
- **Request Bodies**: Bodies containing "password" are not logged
- **Size Limits**: Request bodies are truncated to 1000 characters

## Log Formats

### JSON Format (Structured)

When `log_json` is enabled, logs are output in structured JSON format:

```json
{
  "timestamp": "2024-01-15T10:30:45.123456",
  "level": "INFO",
  "logger": "app.main",
  "message": "User logged in successfully",
  "module": "auth",
  "function": "login",
  "line": 45,
  "process_id": 12345,
  "thread_id": 67890,
  "environment": "production",
  "app_name": "MyApp",
  "app_version": "1.0.0",
  "request_id": "req-abc-123",
  "user_id": "user-456",
  "extra": {
    "user_id": "user-456",
    "ip_address": "192.168.1.100",
    "action": "login"
  }
}
```

### Human-Readable Format (Console)

For console output with colors enabled:

```
2024-01-15 10:30:45.123 | INFO     | app.main:login:45 | User logged in successfully
2024-01-15 10:30:46.456 | WARNING  | app.auth:validate:78 | Invalid token provided
2024-01-15 10:30:47.789 | ERROR    | app.db:connect:12 | Database connection failed
```

## File Organization

The logger creates several log files:

```
logs/
├── app.log              # Main application logs
├── app.log.1.gz         # Rotated logs (compressed)
├── app.log.2.gz         # Older rotated logs
├── exceptions.log       # Exception-only logs
├── exceptions.log.1.gz  # Rotated exception logs
└── requests.log         # HTTP request logs (separate)
    ├── requests.log.1.gz
    └── requests.log.2.gz
```

## Performance Considerations

### Best Practices

1. **Use Appropriate Log Levels**:
   ```python
   # Good - only logged in DEBUG mode
   logger.debug("Detailed debugging info")
   
   # Good - important information
   logger.info("User action completed")
   
   # Good - problems that should be investigated
   logger.warning("Deprecated API used")
   ```

2. **Leverage Structured Logging**:
   ```python
   # Good - searchable and analyzable
   logger.info("Order processed", extra={
       "order_id": "ORD-123",
       "customer_id": "CUST-456",
       "amount": 99.99,
       "status": "completed"
   })
   
   # Avoid - hard to parse
   logger.info(f"Order ORD-123 for customer CUST-456 processed for $99.99")
   ```

3. **Use Context Managers for Performance**:
   ```python
   # Automatic timing and error handling
   with LogPerformance("database_migration", table_count=50):
       migrate_database()
   ```

### Performance Features

- **Enqueued Logging**: Non-blocking log writing for high-throughput applications
- **Compression**: Automatic gzip compression for rotated logs
- **Rotation**: Size and time-based log rotation to manage disk space
- **Filtering**: Efficient log filtering to reduce I/O operations

## Integration Examples

### FastAPI Application

```python
from fastapi import FastAPI, Request
from app.utils.logger.setup import setup_logging, add_logging_middleware
from app.utils.logger.logger_config import LoggerUtils
from app.config.settings import settings
from loguru import logger

# Initialize FastAPI app
app = FastAPI()

# Setup logging
setup_logging(settings)

# Add logging middleware
add_logging_middleware(app, settings)

@app.get("/api/users/{user_id}")
async def get_user(user_id: str, request: Request):
    # Request context is automatically set by middleware
    logger.info(f"Fetching user details", extra={"user_id": user_id})
    
    try:
        # Simulate business logic
        with LogPerformance("user_lookup", user_id=user_id):
            user = await fetch_user_from_db(user_id)
        
        LoggerUtils.log_business_event("user_viewed", 
            user_id=user_id,
            viewer_role="admin"
        )
        
        return {"user": user}
        
    except UserNotFound:
        logger.warning(f"User not found", extra={"user_id": user_id})
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        logger.exception("Failed to fetch user", extra={"user_id": user_id})
        raise HTTPException(status_code=500, detail="Internal server error")
```

### Background Tasks

```python
from app.utils.logger.logger_config import LoggerUtils
from loguru import logger
import asyncio

async def background_task():
    # Generate unique context for background task
    task_id = str(uuid.uuid4())
    LoggerUtils.set_request_context(request_id=task_id)
    
    try:
        logger.info("Background task started", extra={"task_type": "data_sync"})
        
        with LogPerformance("data_synchronization", records_count=1000):
            await sync_data()
        
        LoggerUtils.log_business_event("data_sync_completed",
            records_synced=1000,
            sync_duration=30.5
        )
        
    except Exception as e:
        logger.exception("Background task failed")
    finally:
        LoggerUtils.clear_request_context()
```

## Troubleshooting

### Common Issues

1. **Logs Not Appearing**:
   - Check `LOG_LEVEL` setting
   - Verify `LOG_CONSOLE` is enabled for console output
   - Ensure log directory is writable

2. **Large Log Files**:
   - Configure `LOG_ROTATION` (e.g., "100 MB", "1 day")
   - Set appropriate `LOG_RETENTION` period
   - Enable `LOG_COMPRESSION`

3. **Performance Issues**:
   - Reduce log level in production
   - Enable JSON logging only when needed
   - Use async logging (enabled by default)

4. **Missing Request Context**:
   - Ensure middleware is properly configured
   - Manually set context for background tasks
   - Call `LoggerUtils.clear_request_context()` in finally blocks

### Debug Mode

Enable debug mode for troubleshooting:

```python
# In settings
debug: bool = True
log_level: str = "DEBUG"
log_backtrace: bool = True
```

This will:
- Show detailed log information
- Include file paths and line numbers
- Show full backtraces for exceptions
- Enable diagnostic information

## Advanced Configuration

### Custom Log Filters

```python
from loguru import logger

# Filter out health check logs
def filter_health_checks(record):
    return "health" not in record["message"].lower()

logger.add("app.log", filter=filter_health_checks)
```

### Custom Formatters

```python
from app.utils.logger.logger_config import CustomFormatter

# Create custom formatter with additional fields
class MyCustomFormatter(CustomFormatter):
    def format(self, record):
        log_data = super().format(record)
        # Add custom fields
        parsed_data = json.loads(log_data)
        parsed_data["custom_field"] = "custom_value"
        return json.dumps(parsed_data)
```

### Multiple Log Destinations

```python
from loguru import logger

# Add multiple destinations
logger.add("app.log", level="INFO")           # General logs
logger.add("errors.log", level="ERROR")       # Error logs only  
logger.add("debug.log", level="DEBUG")        # Debug logs
```

## Migration Guide

### From Standard Python Logging

```python
# Old way
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# New way  
from app.utils.logger.setup import setup_logging
from app.config.settings import settings
logger = setup_logging(settings)
```

### From Basic Loguru

```python
# Old way
from loguru import logger
logger.add("file.log")

# New way - with full configuration
from app.utils.logger.setup import setup_logging
from app.config.settings import settings
logger = setup_logging(settings)
```

## Monitoring and Alerting

### Log Aggregation

The structured JSON format is perfect for log aggregation systems:

- **ELK Stack**: Elasticsearch, Logstash, Kibana
- **Fluentd**: Log collection and forwarding
- **Grafana Loki**: Log aggregation system
- **Datadog**: Cloud monitoring platform

### Metrics Extraction

Extract metrics from logs:

```python
# Performance metrics
duration_metric = log_entry["extra"]["duration"]

# Business metrics  
payment_amount = log_entry["extra"]["amount"]

# Error rates
error_count = len([log for log in logs if log["level"] == "ERROR"])
```

## Security Considerations

### Data Privacy

- Sensitive headers are automatically redacted
- Request bodies containing passwords are not logged
- User IDs are logged but can be hashed if needed
- IP addresses are logged for security monitoring

### GDPR Compliance

Configure retention periods to comply with data protection regulations:

```python
# settings.py
log_retention: str = "30 days"      # Adjust based on requirements
log_exception_retention: str = "90 days"  # Keep exceptions longer for debugging
```

## Conclusion

This logging system provides enterprise-grade logging capabilities with:

- **Production Ready**: Thread-safe, performant, and reliable
- **Developer Friendly**: Easy to use with sensible defaults  
- **Highly Configurable**: Extensive configuration options
- **Monitoring Ready**: Structured output perfect for analysis
- **Security Conscious**: Automatic sensitive data protection

For support or feature requests, please refer to the project documentation or contact the development team.
