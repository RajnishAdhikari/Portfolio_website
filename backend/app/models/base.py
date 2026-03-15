"""
Base Model for All Database Models
=================================

This module provides the abstract base model that all database models inherit from.
It implements common patterns used across the entire application.

Features:
    - UUID primary keys for better distribution and security
    - Automatic timestamp tracking (created_at, updated_at)
    - Soft delete support (is_deleted flag)
    - Consistent field names across all models

Design Decisions:
    - UUID vs Integer IDs: UUIDs prevent ID enumeration attacks and allow
      for distributed ID generation without conflicts
    - Soft Delete: Preserves data for audit trails and prevents cascade deletions
    - Timestamps: Automatic tracking of when records are created and modified

Usage:
    from app.models.base import BaseModel
    
    class MyModel(BaseModel):
        __tablename__ = "my_table"
        name = Column(String(255))
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean
from ..database import Base


class BaseModel(Base):
    """
    Abstract base model with common fields for all database tables.
    
    This class should never be instantiated directly - it's an abstract base
    that provides common functionality to all models in the application.
    
    Attributes:
        id (str): UUID primary key as string for better portability
        created_at (datetime): Timestamp when record was created (auto-set)
        updated_at (datetime): Timestamp when record was last modified (auto-updated)
        is_deleted (bool): Soft delete flag (True = deleted, False = active)
        
    Example:
        class User(BaseModel):
            __tablename__ = "users"
            email = Column(String(255))
    """
    
    # Mark as abstract - SQLAlchemy won't create a table for this class
    __abstract__ = True
    
    # ========================================================================
    # PRIMARY KEY
    # ========================================================================
    
    id = Column(
        String(36),          # UUID stored as 36-character string
        primary_key=True,    # Unique identifier for each record
        default=lambda: str(uuid.uuid4()),  # Auto-generate new UUID
        index=True           # Index for faster lookups
    )
    """
    Universal unique identifier (UUID) for the record.
    
    Stored as string for better database portability.
    Automatically generated on record creation.
    """
    
    # ========================================================================
    # TIMESTAMPS
    # ========================================================================
    
    created_at = Column(
        DateTime,
        default=datetime.utcnow,  # Set to current UTC time on creation
        nullable=False            # Must always have a value
    )
    """
    Timestamp when the record was created.
    
    Automatically set to current UTC time when record is first saved.
    Never changes after creation.
    """
    
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,    # Set initially to creation time
        onupdate=datetime.utcnow,   # Update to current time on any modification
        nullable=False              # Must always have a value
    )
    """
    Timestamp when the record was last updated.
    
    Automatically updated to current UTC time whenever the record is modified.
    Useful for tracking when data changes occurred.
    """
    
    # ========================================================================
    # SOFT DELETE
    # ========================================================================
    
    is_deleted = Column(
        Boolean,
        default=False,    # Records start as active (not deleted)
        nullable=False,   # Must always have a value
        index=True        # Index for fast filtering of active records
    )
    """
    Soft delete flag indicating if record is logically deleted.
    
    Instead of physically removing records from the database:
    - Set is_deleted = True to hide the record
    - Queries should filter WHERE is_deleted = False
    - Preserves data for audit trails and prevents cascade issues
    - Can be un-deleted by setting back to False
    """
