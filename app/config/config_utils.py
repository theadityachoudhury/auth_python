"""
Settings usage examples and utilities
"""

from app.config.settings import settings
from typing import Dict, Any, List

def get_cors_config() -> Dict[str, Any]:
    """Get CORS configuration for FastAPI"""
    return {
        "allow_origins": settings.get_allow_origins_list(),
        "allow_credentials": settings.allow_credentials,
        "allow_methods": settings.get_allow_methods_list(),
        "allow_headers": settings.get_allow_headers_list(),
    }

def get_trusted_hosts() -> List[str]:
    """Get trusted hosts for FastAPI"""
    return settings.get_trusted_hosts_list()

def get_database_config() -> Dict[str, Any]:
    """Get database configuration"""
    return {
        "url": settings.database_url,
        "echo": settings.database_echo,
        "pool_size": settings.database_pool_size,
        "max_overflow": settings.database_max_overflow,
        "connect_args": {"check_same_thread": settings.database_check_same_thread} if "sqlite" in settings.database_url else {}
    }

def get_jwt_config() -> Dict[str, Any]:
    """Get JWT configuration"""
    return {
        "secret_key": settings.jwt_secret_key or settings.secret_key,
        "algorithm": settings.jwt_algorithm,
        "access_token_expire_minutes": settings.jwt_access_token_expire_minutes,
        "refresh_token_expire_days": settings.jwt_refresh_token_expire_days,
    }

def get_logging_config() -> Dict[str, Any]:
    """Get logging configuration for Loguru"""
    return {
        "level": settings.log_level,
        "format": settings.log_format,
        "rotation": settings.log_rotation,
        "retention": settings.log_retention,
        "compression": settings.log_compression,
        "backtrace": settings.log_backtrace,
        "colorize": settings.log_color,
        "serialize": settings.log_json,
    }

def get_server_config() -> Dict[str, Any]:
    """Get server configuration for Uvicorn"""
    return {
        "host": settings.host,
        "port": settings.port,
        "reload": settings.reload and settings.debug,
        "debug": settings.debug,
        "log_level": settings.log_level.lower(),
    }

def is_production() -> bool:
    """Check if running in production environment"""
    return settings.environment.lower() == "production"

def is_development() -> bool:
    """Check if running in development environment"""
    return settings.environment.lower() == "development"

def is_testing() -> bool:
    """Check if running in testing environment"""
    return settings.environment.lower() == "testing"

# Example usage in FastAPI main.py
def get_app_metadata() -> Dict[str, Any]:
    """Get application metadata for FastAPI"""
    return {
        "title": settings.app_name,
        "description": settings.app_description,
        "version": settings.app_version,
        "contact": {
            "name": settings.app_author,
            "url": settings.app_contact,
            "email": settings.app_contact_email,
        } if settings.app_contact or settings.app_contact_email else None,
        "license_info": {
            "name": settings.app_license,
        } if settings.app_license else None,
    }

# Example usage functions
if __name__ == "__main__":
    print("Configuration Usage Examples:")
    print("=" * 40)
    
    print("\n📱 App Metadata:")
    metadata = get_app_metadata()
    for key, value in metadata.items():
        print(f"   {key}: {value}")
    
    print("\n🌐 CORS Config:")
    cors = get_cors_config()
    for key, value in cors.items():
        print(f"   {key}: {value}")
    
    print(f"\n🔐 JWT Config:")
    jwt = get_jwt_config()
    for key, value in jwt.items():
        if "secret" in key.lower():
            print(f"   {key}: {'***' if value else 'None'}")
        else:
            print(f"   {key}: {value}")
    
    print(f"\n🖥️ Server Config:")
    server = get_server_config()
    for key, value in server.items():
        print(f"   {key}: {value}")
    
    print(f"\n💾 Database Config:")
    db = get_database_config()
    for key, value in db.items():
        if "url" in key.lower() and "sqlite" not in str(value).lower():
            # Mask database credentials for security
            print(f"   {key}: {'***masked***' if '://' in str(value) else value}")
        else:
            print(f"   {key}: {value}")
    
    print(f"\n🌍 Environment Checks:")
    print(f"   Is Production: {is_production()}")
    print(f"   Is Development: {is_development()}")
    print(f"   Is Testing: {is_testing()}")
