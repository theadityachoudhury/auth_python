from loguru import logger

async def shutdown_event():
    """
    Shutdown event handler for the FastAPI application.
    This function is called when the application is shutting down.
    """
    logger.info("Application is shutting down...")
    logger.info("Cleanup operations completed")
    logger.warning("Application shutdown completed")