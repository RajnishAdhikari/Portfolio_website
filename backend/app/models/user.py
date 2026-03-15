"""
User Model for Authentication and Authorization
=============================================

This module defines the User model for authentication and role-based access control.

Features:
    - Email-based authentication
    - Password hashing (never store plain text passwords)
    - Role-based access (Admin vs Contributor)
    - Unique email constraint
    
Roles:
    - ADMIN: Full access to create, read, update, delete all content
    - CONTRIBUTOR: Limited access (can be configured per endpoint)

Security:
    - Passwords are hashed using passlib with bcrypt
    - Emails are unique and indexed for fast lookups
    - JWT tokens are used for stateless authentication
"""

from sqlalchemy import Column, String, Enum
from .base import BaseModel
import enum


# ============================================================================
# ENUMERATIONS
# ============================================================================

class UserRole(str, enum.Enum):
    """
    User role enumeration for access control.
    
    Roles determine what actions a user can perform:
    - ADMIN: Full CRUD access to all resources
    - CONTRIBUTOR: Limited access to specific resources
    
    Stored as strings in database for better readability and flexibility.
    """
    ADMIN = "admin"
    CONTRIBUTOR = "contributor"


# ============================================================================
# USER MODEL
# ============================================================================

class User(BaseModel):
    """
    User model for authentication and authorization.
    
    Represents registered users who can access admin/protected endpoints.
    Inherits UUID, timestamps, and soft delete from BaseModel.
    
    Attributes:
        email (str): User's email address (unique, required)
        hashed_password (str): Bcrypt-hashed password (required)
        role (UserRole): Access level (admin or contributor)
        
    Example:
        from app.core.security import get_password_hash
        
        user = User(
            email="admin@example.com",
            hashed_password=get_password_hash("securepassword"),
            role=UserRole.ADMIN
        )
        db.add(user)
        db.commit()
    """
    
    __tablename__ = "users"
    
    # ========================================================================
    # AUTHENTICATION FIELDS
    # ========================================================================
    
    email = Column(
        String(255),
        unique=True,      # Each email can only register once
        nullable=False,   # Email is required
        index=True        # Index for fast email lookups during login
    )
    """
    User's email address for authentication.
    
    Must be unique across all users. Used as primary identifier for login.
    Indexed for fast lookups during authentication.
    """
    
    hashed_password = Column(
        String(255),
        nullable=False    # Password is required
    )
    """
    Bcrypt-hashed password.
    
    Never stores plain text passwords for security.
    Hash is generated using passlib's bcrypt algorithm.
    Minimum recommended length: 60 characters for bcrypt hash.
    """
    
    # ========================================================================
    # AUTHORIZATION FIELDS
    # ========================================================================
    
    role = Column(
        Enum(UserRole, values_callable=lambda x: [e.value for e in x]),
        default=UserRole.CONTRIBUTOR,  # New users default to contributor
        nullable=False                 # Role is required
    )
    """
    User's role for authorization.
    
    Determines what actions the user can perform:
    - ADMIN: Can create, update, delete all content
    - CONTRIBUTOR: Limited permissions (configured per endpoint)
    
    Uses values_callable to store lowercase string values ("admin", "contributor")
    instead of uppercase enum names for better database readability.
    """
