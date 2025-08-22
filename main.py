"""
FastAPI application entry point.

This file imports the application from the app module.
The actual application logic is now organized in the app/ directory.
"""

from app.main import app

# Export the app for uvicorn
__all__ = ["app"]