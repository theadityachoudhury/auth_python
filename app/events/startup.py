from loguru import logger

async def startup_event():
    """
    Startup event handler for the FastAPI application.
    This function is called when the application starts.
    """
    logger.info("Application is starting up...")
    logger.info("Startup event completed successfully")
    
    # Test different log levels
    logger.debug("Debug message during startup")
    logger.warning("This is a test warning message")
    
    # Test extra data
    logger.info("Application configuration loaded", extra={
        "config_status": "loaded",
        "startup_phase": "initialization"
    })