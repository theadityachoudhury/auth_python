from loguru import logger
from app.config.database import db_health_check, init_db

async def startup_event():
    """
    Startup event handler for the FastAPI application.
    This function is called when the application starts.
    """
    logger.info("Application is starting up...")
    logger.info("Startup event completed successfully")
    
    logger.info("Connecting to the database...")
    try:
        init_db()
        health = db_health_check()
        logger.info(f"Database health status: {health}")
        logger.info("Database connection established successfully")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        raise e
    
    
    # Test different log levels
    logger.debug("Debug message during startup")
    logger.warning("This is a test warning message")
    
    # Test extra data
    logger.info("Application configuration loaded", extra={
        "config_status": "loaded",
        "startup_phase": "initialization"
    })