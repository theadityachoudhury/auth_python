#!/usr/bin/env python3
"""
Configuration Test Script
Tests if all environment variables are properly loaded and configuration is valid.
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_configuration():
    """Test the configuration settings"""
    try:
        from app.config.settings import settings
        
        print("🔧 Configuration Test Results")
        print("=" * 50)
        
        # Application Settings
        print(f"📱 App Name: {settings.app_name}")
        print(f"📝 App Description: {settings.app_description}")
        print(f"🏷️  App Version: {settings.app_version}")
        print(f"👤 App Author: {settings.app_author}")
        print(f"🌍 Environment: {settings.environment}")
        print(f"🐛 Debug Mode: {settings.debug}")
        
        # Server Settings
        print(f"\n🖥️  Server Configuration:")
        print(f"   Host: {settings.host}")
        print(f"   Port: {settings.port}")
        print(f"   Reload: {settings.reload}")
        
        # Security Settings
        print(f"\n🔐 Security Configuration:")
        print(f"   Secret Key: {'***' if settings.secret_key != 'your-super-secret-key-change-this-in-production' else '⚠️  DEFAULT KEY - CHANGE THIS!'}")
        print(f"   JWT Algorithm: {settings.jwt_algorithm}")
        print(f"   Token Expiry: {settings.jwt_access_token_expire_minutes} minutes")
        
        # Database Settings
        print(f"\n💾 Database Configuration:")
        print(f"   Database URL: {settings.database_url}")
        print(f"   Echo SQL: {settings.database_echo}")
        print(f"   Pool Size: {settings.database_pool_size}")
        
        # Logging Settings
        print(f"\n📊 Logging Configuration:")
        print(f"   Log Level: {settings.log_level}")
        print(f"   Log File: {settings.log_file}")
        print(f"   JSON Format: {settings.log_json}")
        print(f"   Console Output: {settings.log_console}")
        
        # CORS Settings
        print(f"\n🌐 CORS Configuration:")
        print(f"   Allowed Origins: {settings.get_allow_origins_list()}")
        print(f"   Allow Credentials: {settings.allow_credentials}")
        
        # Validation Warnings
        print(f"\n⚠️  Configuration Warnings:")
        warnings = []
        
        if settings.debug and settings.environment == "production":
            warnings.append("Debug mode is enabled in production environment")
            
        if settings.secret_key == "your-super-secret-key-change-this-in-production":
            warnings.append("Using default secret key - change this for security")
            
        if settings.jwt_secret_key == settings.secret_key:
            warnings.append("JWT secret key is same as app secret key - consider using different keys")
            
        if "*" in settings.get_allow_origins_list() and settings.environment == "production":
            warnings.append("CORS allows all origins in production - consider restricting")
            
        if not warnings:
            print("   ✅ No configuration warnings")
        else:
            for warning in warnings:
                print(f"   ⚠️  {warning}")
        
        print(f"\n✅ Configuration loaded successfully!")
        return True
        
    except ImportError as e:
        print(f"❌ Failed to import settings: {e}")
        print("Make sure you've installed all dependencies: pip install -r requirements.txt")
        return False
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def check_env_file():
    """Check if .env file exists and has required variables"""
    env_path = Path(".env")
    
    if not env_path.exists():
        print("⚠️  .env file not found - using default values")
        return False
        
    print("✅ .env file found")
    
    required_vars = [
        "SECRET_KEY",
        "DATABASE_URL",
        "APP_NAME"
    ]
    
    missing_vars = []
    with open(env_path, 'r') as f:
        content = f.read()
        for var in required_vars:
            if f"{var}=" not in content:
                missing_vars.append(var)
    
    if missing_vars:
        print(f"⚠️  Missing environment variables: {', '.join(missing_vars)}")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 Starting Configuration Test\n")
    
    # Check .env file
    env_ok = check_env_file()
    
    # Test configuration
    config_ok = test_configuration()
    
    if config_ok and env_ok:
        print(f"\n🎉 All tests passed! Your configuration is ready to use.")
        sys.exit(0)
    else:
        print(f"\n❌ Some tests failed. Please check the issues above.")
        sys.exit(1)
