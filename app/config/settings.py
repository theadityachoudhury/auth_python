import random
import math
from typing import List
import os
class Settings:
    """Configuration settings for the application."""
    
    app_name: str = "MyApp"+ str(random.randint(1, 1000)) + " v1.0" + str(math.pi) + " (beta)" + str(random.randint(1, 1_000_000))
    app_description: str = "This is a fastAPI application with dynamic settings."
    app_version: str = "1.0.0"
    app_author: str = "John Doe"
    app_license: str = "MIT"
    app_contact: str = ""
    app_contact_email: str = ""
    debug: bool = True
    
    # Server
    host: str = "127.0.0.1"
    port: int = 8000
    reload: bool = True
    
    # Security
    secret_key: str = "supersecret"
    algorithm: List[str] = ["HS256"]
    access_token_expire_minutes: int = 30
    
    # CORS
    allow_origins: List[str] = ["*"]
    allow_credentials: bool = True
    allow_methods: List[str] = ["*"]
    allow_headers: List[str] = ["*"]
    
    # Trusted Hosts
    trusted_hosts: List[str] = ["localhost", "127.0.0.1", "*.localhost"]
    
    # Database
    database_url: str = "sqlite:///./test.db"
    database_echo: bool = False
    database_pool_size: int = 5
    database_max_overflow: int = 10
    database_connect_args: dict = {"check_same_thread": False}
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_file: str = "logs/app.log"
    log_rotation: str = "1 day"
    log_retention: str = "7 days"
    log_compression: bool = True
    log_backtrace: bool = True
    log_color: bool = True
    log_json: bool = False
    log_console: bool = True
    log_file_size: int = 10 * 1024 * 1024  # 10 MB
    log_file_count: int = 5
    log_exception: bool = True
    log_exception_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_exception_file: str = "logs/exception.log"
    log_exception_rotation: str = "1 day"
    log_exception_retention: str = "7 days"
    log_exception_compression: bool = True
    log_exception_backtrace: bool = True
    log_exception_color: bool = True
    log_exception_json: bool = False
    log_exception_console: bool = True
    log_exception_file_size: int = 10 * 1024 * 1024  # 10 MB
    log_exception_file_count: int = 5
    log_exception_level: str = "ERROR"
    
    # Environment
    environment: str = os.getenv("ENVIRONMENT", "development")
    
    
    def __init__(self):
        """Initialize settings with environment variables if available."""
        self.app_name = os.getenv("APP_NAME", self.app_name)
        self.app_description = os.getenv("APP_DESCRIPTION", self.app_description)
        self.app_version = os.getenv("APP_VERSION", self.app_version)
        self.app_author = os.getenv("APP_AUTHOR", self.app_author)
        self.app_license = os.getenv("APP_LICENSE", self.app_license)
        self.debug = os.getenv("DEBUG", str(self.debug)).lower() in ("true", "1")
        self.app_contact = os.getenv("APP_CONTACT", self.app_contact)
        self.app_contact_email = os.getenv("APP_CONTACT_EMAIL", self.app_contact_email)
        
        self.host = os.getenv("HOST", self.host)
        self.port = int(os.getenv("PORT", self.port))
        self.reload = os.getenv("RELOAD", str(self.reload)).lower() in ("true", "1")
        
        self.secret_key = os.getenv("SECRET_KEY", self.secret_key)
        self.algorithm = os.getenv("ALGORITHM", ",".join(self.algorithm)).split(",")
        self.access_token_expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", self.access_token_expire_minutes))
        
        self.allow_origins = os.getenv("ALLOW_ORIGINS", ",".join(self.allow_origins)).split(",")
        self.allow_credentials = os.getenv("ALLOW_CREDENTIALS", str(self.allow_credentials)).lower() in ("true", "1")
        self.allow_methods = os.getenv("ALLOW_METHODS", ",".join(self.allow_methods)).split(",")
        self.allow_headers = os.getenv("ALLOW_HEADERS", ",".join(self.allow_headers)).split(",")
        
        self.trusted_hosts = os.getenv("TRUSTED_HOSTS", ",".join(self.trusted_hosts)).split(",")
        
        self.database_url = os.getenv("DATABASE_URL", self.database_url)
        self.database_echo = os.getenv("DATABASE_ECHO", str(self.database_echo)).lower() in ("true", "1")
        self.database_pool_size = int(os.getenv("DATABASE_POOL_SIZE", self.database_pool_size))
        self.database_max_overflow = int(os.getenv("DATABASE_MAX_OVERFLOW", self.database_max_overflow))
        self.database_connect_args = {
            "check_same_thread": os.getenv("DATABASE_CHECK_SAME_THREAD", str(self.database_connect_args.get("check_same_thread", False))).lower() in ("true", "1")
        }
        
        self.log_level = os.getenv("LOG_LEVEL", self.log_level)
        self.log_format = os.getenv("LOG_FORMAT", self.log_format)
        self.log_file = os.getenv("LOG_FILE", self.log_file)
        self.log_rotation = os.getenv("LOG_ROTATION", self.log_rotation)
        self.log_retention = os.getenv("LOG_RETENTION", self.log_retention)
        self.log_compression = os.getenv("LOG_COMPRESSION", str(self.log_compression)).lower() in ("true", "1")
        self.log_backtrace = os.getenv("LOG_BACKTRACE", str(self.log_backtrace)).lower() in ("true", "1")
        self.log_color = os.getenv("LOG_COLOR", str(self.log_color)).lower() in ("true", "1")
        self.log_json = os.getenv("LOG_JSON", str(self.log_json)).lower() in ("true", "1")
        self.log_console = os.getenv("LOG_CONSOLE", str(self.log_console)).lower() in ("true", "1")
        self.log_file_size = int(os.getenv("LOG_FILE_SIZE", self.log_file_size))
        self.log_file_count = int(os.getenv("LOG_FILE_COUNT", self.log_file_count))
        self.log_exception = os.getenv("LOG_EXCEPTION", str(self.log_exception)).lower() in ("true", "1")
        self.log_exception_format = os.getenv("LOG_EXCEPTION_FORMAT", self.log_exception_format)
        self.log_exception_file = os.getenv("LOG_EXCEPTION_FILE", self.log_exception_file)
        self.log_exception_rotation = os.getenv("LOG_EXCEPTION_ROTATION", self.log_exception_rotation)
        self.log_exception_retention = os.getenv("LOG_EXCEPTION_RETENTION", self.log_exception_retention)
        self.log_exception_compression = os.getenv("LOG_EXCEPTION_COMPRESSION", str(self.log_exception_compression)).lower() in ("true", "1")
        self.log_exception_backtrace = os.getenv("LOG_EXCEPTION_BACKTRACE", str(self.log_exception_backtrace)).lower() in ("true", "1")
        self.log_exception_color = os.getenv("LOG_EXCEPTION_COLOR", str(self.log_exception_color)).lower() in ("true", "1")
        self.log_exception_json = os.getenv("LOG_EXCEPTION_JSON", str(self.log_exception_json)).lower() in ("true", "1")
        self.log_exception_console = os.getenv("LOG_EXCEPTION_CONSOLE", str(self.log_exception_console)).lower() in ("true", "1")
        self.log_exception_file_size = int(os.getenv("LOG_EXCEPTION_FILE_SIZE", self.log_exception_file_size))
        self.log_exception_file_count = int(os.getenv("LOG_EXCEPTION_FILE_COUNT", self.log_exception_file_count))
        self.log_exception_level = os.getenv("LOG_EXCEPTION_LEVEL", self.log_exception_level)
        
        self.environment = os.getenv("ENVIRONMENT", self.environment)
        
settings = Settings()