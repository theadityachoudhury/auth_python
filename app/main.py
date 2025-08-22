from fastapi import FastAPI
from app.events.startup import startup_event
from app.events.shutdown import shutdown_event
from app.config.settings import settings as Settings
from dotenv import load_dotenv
from app.utils.logger.setup import setup_logging, add_logging_middleware
from loguru import logger

def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    """
    app = FastAPI(
        title=Settings.app_name,
        description=Settings.app_description,
        version=Settings.app_version,
        openapi_url="/api/v1/openapi.json",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        debug=Settings.debug,
        callbacks=None,
        lifespan=None,
        on_shutdown=[shutdown_event],
        on_startup=[startup_event],
        webhooks=None,
        dependencies=None
    )
    
    # Setup Middlewares
    add_logging_middleware(app, Settings)
    
    # Setup Routers
    
    
    @app.get("/test-logs")
    async def test_logs():
        logger.debug("Debug log from test endpoint")
        logger.info("Info log from test endpoint")
        logger.warning("Warning log from test endpoint")
        
        # Test with extra data
        logger.info("Test log with extra data", extra={
            "endpoint": "/test-logs",
            "action": "test_logging",
            "user_id": "test-user-123"
        })
        
        try:
            # Simulate an error for exception logging
            result = 1 / 0
        except Exception as e:
            logger.error("Test error occurred", extra={"error_type": "division_by_zero"})
            # Don't re-raise, just log it for testing
        
        return {"message": "Logs generated successfully", "check": "logs directory"}

    return app

# Loading environment variables
load_dotenv()

setup_logging(Settings)

app = create_app()