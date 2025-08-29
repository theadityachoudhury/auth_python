from loguru import logger
from app.config.settings import settings
from app.config.database import close_db
from app.utils.pycache_cleanup import cleanup_pycache

async def shutdown_event():
    """
    Shutdown event handler for the FastAPI application.
    This function is called when the application is shutting down.
    """
    logger.info("Application is shutting down...")
    logger.info("Performing cleanup operations...")
    
    logger.info("Closing database connections...")
    close_db()
    
    logger.info("Cleaning up temporary files and caches...")
    
    # Clean up __pycache__ folders only in development mode
    if settings.environment.lower() in ['development', 'dev'] or settings.debug:
        await cleanup_pycache()
    else:
        logger.info("Skipping __pycache__ cleanup (not in development mode)")
    
    logger.info("Cleanup operations completed")
    logger.warning("Application shutdown completed")

