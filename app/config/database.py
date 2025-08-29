from sqlalchemy import create_engine, event, text, Engine
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool, QueuePool
from sqlalchemy.exc import SQLAlchemyError, DisconnectionError
from contextlib import contextmanager
from typing import Generator, Optional, Dict, Any, Type
import logging
import time
from .settings import settings

# Configure logger
logger = logging.getLogger(__name__)

class DatabaseManager:
    """Enhanced database manager with connection pooling, health checks, and error handling."""
    
    def __init__(self):
        self._engine: Optional[Engine] = None
        self._session_factory: Optional[sessionmaker] = None
        self._base: Optional[Type[DeclarativeMeta]] = None
        self._is_initialized = False
        self._connection_retry_attempts = 3
        self._connection_retry_delay = 1.0
    
    @property
    def engine(self) -> Engine:
        """Get the database engine, initializing if necessary."""
        if not self._is_initialized:
            self._initialize()
        if self._engine is None:
            raise RuntimeError("Database engine not initialized")
        return self._engine
    
    @property
    def session_factory(self) -> sessionmaker:
        """Get the session factory, initializing if necessary."""
        if not self._is_initialized:
            self._initialize()
        if self._session_factory is None:
            raise RuntimeError("Session factory not initialized")
        return self._session_factory
    
    @property
    def base(self) -> Type[DeclarativeMeta]:
        """Get the declarative base, initializing if necessary."""
        if not self._is_initialized:
            self._initialize()
        if self._base is None:
            raise RuntimeError("Declarative base not initialized")
        return self._base
    
    def _get_engine_config(self) -> Dict[str, Any]:
        """Get engine configuration based on database type."""
        config = {
            "pool_pre_ping": True,
            "echo": settings.database_echo,
            "pool_size": settings.database_pool_size,
            "max_overflow": settings.database_max_overflow,
            "pool_recycle": 3600,  # Recycle connections every hour
            "pool_timeout": 30,    # Timeout after 30 seconds
        }
        
        # Database-specific configurations
        if "sqlite" in settings.database_url.lower():
            config.update({
                "connect_args": {
                    "check_same_thread": settings.database_check_same_thread,
                    "timeout": 20,
                    "isolation_level": None,  # Autocommit mode
                },
                "poolclass": StaticPool,
                "pool_size": 1,  # SQLite doesn't benefit from multiple connections
                "max_overflow": 0,
            })
        elif "postgresql" in settings.database_url.lower():
            config.update({
                "connect_args": {
                    "connect_timeout": 10,
                    "application_name": settings.app_name,
                },
                "poolclass": QueuePool,
                "pool_reset_on_return": "commit",
            })
        elif "mysql" in settings.database_url.lower():
            config.update({
                "connect_args": {
                    "connect_timeout": 10,
                    "charset": "utf8mb4",
                },
                "poolclass": QueuePool,
                "pool_reset_on_return": "commit",
            })
        
        return config
    
    def _initialize(self):
        """Initialize the database engine and session factory."""
        if self._is_initialized:
            return
        
        try:
            logger.info("Initializing database connection...")
            
            # Create engine with appropriate configuration
            engine_config = self._get_engine_config()
            self._engine = create_engine(settings.database_url, **engine_config)
            
            # Add event listeners
            self._add_event_listeners()
            
            # Create session factory
            self._session_factory = sessionmaker(
                bind=self._engine,
                autocommit=False,
                autoflush=False,
                expire_on_commit=False,  # Keep objects usable after commit
            )
            
            # Create declarative base
            self._base = declarative_base()
            
            # Test the connection
            self._test_connection()
            
            self._is_initialized = True
            logger.info("Database initialization completed successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            self._cleanup()
            raise
    
    def _add_event_listeners(self):
        """Add SQLAlchemy event listeners for connection management."""
        if self._engine is None:
            return
            
        @event.listens_for(self._engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            """Set SQLite pragmas for better performance and integrity."""
            if "sqlite" in settings.database_url.lower():
                cursor = dbapi_connection.cursor()
                cursor.execute("PRAGMA foreign_keys=ON")
                cursor.execute("PRAGMA journal_mode=WAL")
                cursor.execute("PRAGMA synchronous=NORMAL")
                cursor.execute("PRAGMA temp_store=MEMORY")
                cursor.execute("PRAGMA mmap_size=268435456")  # 256MB
                cursor.close()
        
        @event.listens_for(self._engine, "engine_connect")
        def receive_engine_connect(conn, branch):
            """Log successful connections."""
            logger.debug("Database connection established")
        
        @event.listens_for(self._engine, "handle_error")
        def receive_handle_error(exception_context):
            """Handle database errors and connection issues."""
            logger.error(f"Database error: {exception_context.original_exception}")
            
            if isinstance(exception_context.original_exception, DisconnectionError):
                logger.warning("Database disconnection detected, connection will be refreshed")
    
    def _test_connection(self):
        """Test the database connection."""
        if self._engine is None:
            raise RuntimeError("Engine not initialized")
            
        max_retries = self._connection_retry_attempts
        for attempt in range(max_retries):
            try:
                with self._engine.connect() as conn:
                    conn.execute(text("SELECT 1"))
                logger.info("Database connection test successful")
                return
            except Exception as e:
                if attempt < max_retries - 1:
                    logger.warning(f"Connection test attempt {attempt + 1} failed: {e}")
                    time.sleep(self._connection_retry_delay)
                else:
                    logger.error(f"All connection test attempts failed: {e}")
                    raise
    
    def get_session(self) -> Session:
        """Get a new database session."""
        if not self._is_initialized:
            self._initialize()
        if self._session_factory is None:
            raise RuntimeError("Session factory not initialized")
        return self._session_factory()
    
    @contextmanager
    def get_session_context(self) -> Generator[Session, None, None]:
        """Get a database session with automatic cleanup."""
        session = self.get_session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            session.close()
    
    def health_check(self) -> Dict[str, Any]:
        """Perform a health check on the database connection."""
        try:
            if self._engine is None:
                return {
                    "status": "unhealthy",
                    "error": "Database engine not initialized",
                    "database_url": settings.database_url.split("://")[0] + "://***",
                }
            
            start_time = time.time()
            
            with self._engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            
            response_time = time.time() - start_time
            
            # Get basic connection pool info
            pool_info = {}
            try:
                pool = self._engine.pool
                pool_info["pool_type"] = type(pool).__name__
                
                # Try to get pool statistics safely
                try:
                    # Some pools have these as properties, others as methods
                    for attr in ['size', 'checked_in', 'checked_out', 'overflow']:
                        if hasattr(pool, attr):
                            value = getattr(pool, attr)
                            # If it's callable, call it
                            if callable(value):
                                try:
                                    pool_info[attr] = value()
                                except:
                                    pass
                            else:
                                pool_info[attr] = value
                except Exception:
                    pass
                        
            except Exception as pool_error:
                logger.debug(f"Could not get pool info: {pool_error}")
                pool_info = {"error": "Pool info not available"}
            
            return {
                "status": "healthy",
                "response_time_ms": round(response_time * 1000, 2),
                "pool_status": pool_info,
                "database_url": settings.database_url.split("://")[0] + "://***",  # Hide credentials
            }
            
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return {
                "status": "unhealthy",
                "error": str(e),
                "database_url": settings.database_url.split("://")[0] + "://***",
            }
    
    def create_tables(self):
        """Create all database tables."""
        try:
            logger.info("Creating database tables...")
            if self._base is None:
                raise RuntimeError("Declarative base not initialized")
            self._base.metadata.create_all(bind=self.engine)
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Failed to create tables: {e}")
            raise
    
    def drop_tables(self):
        """Drop all database tables."""
        try:
            logger.info("Dropping database tables...")
            if self._base is None:
                raise RuntimeError("Declarative base not initialized")
            self._base.metadata.drop_all(bind=self.engine)
            logger.info("Database tables dropped successfully")
        except Exception as e:
            logger.error(f"Failed to drop tables: {e}")
            raise
    
    def _cleanup(self):
        """Clean up database resources."""
        if self._engine:
            try:
                self._engine.dispose()
                logger.info("Database engine disposed")
            except Exception as e:
                logger.error(f"Error disposing engine: {e}")
        
        self._engine = None
        self._session_factory = None
        self._base = None
        self._is_initialized = False
    
    def close(self):
        """Close all database connections and cleanup resources."""
        logger.info("Closing database connections...")
        self._cleanup()


# Global database manager instance
db_manager = DatabaseManager()

# Backward compatibility - expose traditional objects
engine = db_manager.engine
SessionLocal = db_manager.session_factory
Base = db_manager.base


def get_db() -> Generator[Session, None, None]:
    """
    Dependency function to get database session.
    Used with FastAPI's Depends() for automatic session management.
    """
    session = db_manager.get_session()
    try:
        yield session
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"Database error in get_db: {e}")
        raise
    except Exception as e:
        session.rollback()
        logger.error(f"Unexpected error in get_db: {e}")
        raise
    finally:
        session.close()


def get_db_context():
    """Get database session context manager for manual session management."""
    return db_manager.get_session_context()


def init_db():
    """Initialize database and create tables."""
    try:
        db_manager.create_tables()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise


def close_db():
    """Close database connections."""
    db_manager.close()


def db_health_check() -> Dict[str, Any]:
    """Get database health status."""
    return db_manager.health_check()