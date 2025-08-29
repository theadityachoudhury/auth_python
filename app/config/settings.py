from pydantic_settings import BaseSettings
from pydantic import Field, field_validator
from typing import List, Optional, Any
import os
from pathlib import Path
from pathlib import Path

class Settings(BaseSettings):
    """Configuration settings for the application."""
    
    # Application Settings
    app_name: str = Field(default="Auth Service", description="Application name")
    app_description: str = Field(default="FastAPI Authentication and Authorization Service", description="Application description")
    app_version: str = Field(default="1.0.0", description="Application version")
    app_author: str = Field(default="Aditya Choudhury", description="Application author")
    app_license: str = Field(default="MIT", description="Application license")
    app_contact: str = Field(default="", description="Contact URL")
    app_contact_email: str = Field(default="", description="Contact email")
    
    # Environment
    environment: str = Field(default="development", description="Environment (development, production, testing)")
    debug: bool = Field(default=True, description="Debug mode")
    
    # Server Configuration
    host: str = Field(default="127.0.0.1", description="Server host")
    port: int = Field(default=8000, description="Server port")
    reload: bool = Field(default=True, description="Auto-reload on code changes")
    
    # Security Settings
    secret_key: str = Field(default="your-super-secret-key-change-this-in-production", description="Secret key for signing")
    algorithm: str = Field(default="HS256", description="JWT algorithm")
    access_token_expire_minutes: int = Field(default=30, description="Access token expiration in minutes")
    
    # JWT Settings
    jwt_secret_key: Optional[str] = Field(default=None, description="JWT secret key")
    jwt_algorithm: str = Field(default="HS256", description="JWT algorithm")
    jwt_access_token_expire_minutes: int = Field(default=30, description="JWT access token expiration")
    jwt_refresh_token_expire_days: int = Field(default=7, description="JWT refresh token expiration")
    
    # CORS Settings
    allow_origins: str = Field(default="*", description="Allowed origins for CORS (comma-separated)")
    allow_credentials: bool = Field(default=True, description="Allow credentials for CORS")
    allow_methods: str = Field(default="*", description="Allowed methods for CORS (comma-separated)")
    allow_headers: str = Field(default="*", description="Allowed headers for CORS (comma-separated)")
    
    # Trusted Hosts
    trusted_hosts: str = Field(default="localhost,127.0.0.1,*.localhost", description="Trusted hosts (comma-separated)")
    
    # Database Configuration
    database_url: str = Field(default="sqlite:///./auth.db", description="Database URL")
    database_echo: bool = Field(default=False, description="Echo SQL queries")
    database_pool_size: int = Field(default=5, description="Database connection pool size")
    database_max_overflow: int = Field(default=10, description="Database max overflow connections")
    database_check_same_thread: bool = Field(default=False, description="SQLite check same thread")
    
    # Logging Configuration
    log_level: str = Field(default="INFO", description="Logging level")
    log_format: str = Field(default="%(asctime)s - %(name)s - %(levelname)s - %(message)s", description="Log format")
    log_file: str = Field(default="logs/app.log", description="Log file path")
    log_rotation: str = Field(default="1 day", description="Log rotation")
    log_retention: str = Field(default="7 days", description="Log retention")
    log_compression: bool = Field(default=True, description="Enable log compression")
    log_backtrace: bool = Field(default=True, description="Enable log backtrace")
    log_color: bool = Field(default=True, description="Enable colored logs")
    log_json: bool = Field(default=False, description="Enable JSON logging")
    log_console: bool = Field(default=True, description="Enable console logging")
    log_file_size: int = Field(default=10 * 1024 * 1024, description="Log file size limit")
    log_file_count: int = Field(default=5, description="Number of log files to keep")
    
    # Exception Logging
    log_exception: bool = Field(default=True, description="Enable exception logging")
    log_exception_format: str = Field(default="%(asctime)s - %(name)s - %(levelname)s - %(message)s", description="Exception log format")
    log_exception_file: str = Field(default="logs/exception.log", description="Exception log file")
    log_exception_rotation: str = Field(default="1 day", description="Exception log rotation")
    log_exception_retention: str = Field(default="7 days", description="Exception log retention")
    log_exception_compression: bool = Field(default=True, description="Enable exception log compression")
    log_exception_backtrace: bool = Field(default=True, description="Enable exception backtrace")
    log_exception_color: bool = Field(default=True, description="Enable colored exception logs")
    log_exception_json: bool = Field(default=False, description="Enable JSON exception logging")
    log_exception_console: bool = Field(default=True, description="Enable console exception logging")
    log_exception_file_size: int = Field(default=10 * 1024 * 1024, description="Exception log file size")
    log_exception_file_count: int = Field(default=5, description="Exception log file count")
    log_exception_level: str = Field(default="ERROR", description="Exception log level")
    
    # Email Configuration
    smtp_host: Optional[str] = Field(default=None, description="SMTP server host")
    smtp_port: int = Field(default=587, description="SMTP server port")
    smtp_username: Optional[str] = Field(default=None, description="SMTP username")
    smtp_password: Optional[str] = Field(default=None, description="SMTP password")
    smtp_from_email: Optional[str] = Field(default=None, description="SMTP from email")
    smtp_from_name: Optional[str] = Field(default=None, description="SMTP from name")
    smtp_use_tls: bool = Field(default=True, description="Use TLS for SMTP")
    
    # Redis Configuration
    redis_url: Optional[str] = Field(default=None, description="Redis connection URL")
    redis_password: Optional[str] = Field(default=None, description="Redis password")
    redis_db: int = Field(default=0, description="Redis database number")
    
    # Rate Limiting
    rate_limit_enabled: bool = Field(default=True, description="Enable rate limiting")
    rate_limit_requests_per_minute: int = Field(default=100, description="Requests per minute limit")
    rate_limit_burst: int = Field(default=20, description="Burst limit")
    
    # Password Policy
    password_min_length: int = Field(default=8, description="Minimum password length")
    password_require_uppercase: bool = Field(default=True, description="Require uppercase in password")
    password_require_lowercase: bool = Field(default=True, description="Require lowercase in password")
    password_require_numbers: bool = Field(default=True, description="Require numbers in password")
    password_require_special_chars: bool = Field(default=True, description="Require special characters in password")
    
    # Monitoring
    sentry_dsn: Optional[str] = Field(default=None, description="Sentry DSN for error tracking")
    prometheus_enabled: bool = Field(default=False, description="Enable Prometheus metrics")
    metrics_endpoint: str = Field(default="/metrics", description="Metrics endpoint path")
    
    @field_validator('jwt_secret_key', mode='before')
    @classmethod
    def set_jwt_secret_key(cls, v: Any, info) -> str:
        """Set JWT secret key from secret_key if not provided"""
        if v is None and info.data:
            return info.data.get('secret_key', 'default-secret-key')
        return v or 'default-secret-key'
    
    @field_validator('smtp_from_name', mode='before')
    @classmethod
    def set_smtp_from_name(cls, v: Any, info) -> str:
        """Set SMTP from name from app_name if not provided"""
        if v is None and info.data:
            return info.data.get('app_name', 'Auth Service')
        return v or 'Auth Service'
    
    def get_allow_origins_list(self) -> List[str]:
        """Get allow_origins as a list"""
        if isinstance(self.allow_origins, str):
            return [origin.strip() for origin in self.allow_origins.split(',') if origin.strip()]
        return self.allow_origins if isinstance(self.allow_origins, list) else [self.allow_origins]
    
    def get_allow_methods_list(self) -> List[str]:
        """Get allow_methods as a list"""
        if isinstance(self.allow_methods, str):
            return [method.strip() for method in self.allow_methods.split(',') if method.strip()]
        return self.allow_methods if isinstance(self.allow_methods, list) else [self.allow_methods]
    
    def get_allow_headers_list(self) -> List[str]:
        """Get allow_headers as a list"""
        if isinstance(self.allow_headers, str):
            return [header.strip() for header in self.allow_headers.split(',') if header.strip()]
        return self.allow_headers if isinstance(self.allow_headers, list) else [self.allow_headers]
    
    def get_trusted_hosts_list(self) -> List[str]:
        """Get trusted_hosts as a list"""
        if isinstance(self.trusted_hosts, str):
            return [host.strip() for host in self.trusted_hosts.split(',') if host.strip()]
        return self.trusted_hosts if isinstance(self.trusted_hosts, list) else [self.trusted_hosts]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"

# Create settings instance
settings = Settings()