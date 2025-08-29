from fastapi import FastAPI
from app.events.startup import startup_event
from app.events.shutdown import shutdown_event
from app.config.settings import settings as Settings
from dotenv import load_dotenv
from app.utils.logger.setup import setup_logging, add_logging_middleware
from loguru import logger
from app.routes.routes import api_router

def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    """
    app: FastAPI = FastAPI(
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
    app.include_router(api_router, prefix="/api")

    return app

# Loading environment variables
logger.info("Initializing environment variables", extra={"debug": Settings.debug})
load_dotenv()

setup_logging(Settings)

app = create_app()