"""
Database Configuration and Session Management
============================================

This module handles SQLAlchemy database configuration, connection pooling,
and session management for the portfolio application.

Key Components:
    - Engine: Database connection pool manager
    - SessionLocal: Session factory for creating database sessions
    - Base: Declarative base class for all SQLAlchemy models
    - get_db: Dependency injection function for FastAPI routes

Usage:
    from app.database import get_db, Base
    
    # In FastAPI routes
    @router.get("/items")
    def get_items(db: Session = Depends(get_db)):
        return db.query(Item).all()
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import get_settings

# ============================================================================
# CONFIGURATION
# ============================================================================

# Get application settings (database URL, environment, etc.)
settings = get_settings()

# ============================================================================
# DATABASE ENGINE
# ============================================================================

# Create SQLAlchemy engine with connection pooling
# The engine manages a pool of database connections for efficient reuse
engine = create_engine(
    settings.database_url,
    
    # pool_pre_ping: Verify connections are alive before using them
    # This prevents "MySQL server has gone away" type errors
    pool_pre_ping=True,
    
    # echo: Log all SQL statements - useful for debugging in development
    # Only enabled in dev environment to avoid log pollution in production
    echo=settings.environment == "dev"
)

# ============================================================================
# SESSION FACTORY
# ============================================================================

# Create SessionLocal class - a factory for creating database sessions
# Sessions are the primary interface for persistence operations
SessionLocal = sessionmaker(
    autocommit=False,  # Require explicit commit() calls for safety
    autoflush=False,   # Disable automatic flushing for better control
    bind=engine        # Bind to our database engine
)

# ============================================================================
# BASE MODEL CLASS
# ============================================================================

# Create Base class for all SQLAlchemy models to inherit from
# All models should extend this class to be tracked by SQLAlchemy
Base = declarative_base()


# ============================================================================
# DEPENDENCY INJECTION
# ============================================================================

def get_db():
    """
    Database session dependency for FastAPI routes.
    
    This is a dependency injection function that:
    1. Creates a new database session
    2. Yields it to the route handler
    3. Automatically closes the session when done (even if an error occurs)
    
    Usage:
        @router.get("/items")
        def get_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    
    Yields:
        Session: SQLAlchemy database session
        
    Note:
        The session is automatically closed after the request completes,
        ensuring no connection leaks occur.
    """
    # Create a new session from our factory
    db = SessionLocal()
    
    try:
        # Yield the session to the route handler
        yield db
    finally:
        # Ensure session is closed after request completes
        # This happens even if an exception was raised
        db.close()

