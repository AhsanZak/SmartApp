"""
Database configuration and session management
Uses SQLAlchemy with PostgreSQL and pgvector extension
"""
from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from contextlib import contextmanager

from config.settings import get_settings, get_toml_config


settings = get_settings()

# Create database engine
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    echo=settings.debug
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


# Enable pgvector extension
@event.listens_for(engine, "connect")
def receive_connect(dbapi_conn, connection_record):
    """Enable pgvector extension on connect"""
    with dbapi_conn.cursor() as cursor:
        cursor.execute("CREATE EXTENSION IF NOT EXISTS vector")
        dbapi_conn.commit()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency for getting database session
    
    Yields:
        Database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_context():
    """
    Context manager for database session
    
    Usage:
        with get_db_context() as db:
            # Use db session
            pass
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


class DatabaseManager:
    """Database management utilities"""
    
    @staticmethod
    def init_db():
        """Initialize database tables"""
        Base.metadata.create_all(bind=engine)
    
    @staticmethod
    def drop_db():
        """Drop all database tables"""
        Base.metadata.drop_all(bind=engine)
    
    @staticmethod
    def get_session() -> Session:
        """Get a database session"""
        return SessionLocal()
    
    @staticmethod
    def close_session(session: Session):
        """Close a database session"""
        session.close()


# Database health check
def check_database_connection() -> bool:
    """
    Check if database connection is healthy
    
    Returns:
        True if connection is healthy, False otherwise
    """
    try:
        with engine.connect() as connection:
            connection.execute("SELECT 1")
        return True
    except Exception as e:
        print(f"Database connection error: {e}")
        return False

