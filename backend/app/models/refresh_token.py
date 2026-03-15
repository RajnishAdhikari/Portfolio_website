"""
Refresh Token Model
==================

This module defines the RefreshToken model for secure authentication sessions.
Allows users to stay logged in and request new access tokens without re-entering credentials.

Features:
    - Long-lived session tokens
    - Secure storage (hashed tokens)
    - Expiration handling
    - User association

Security:
    - Tokens are hashed before storage to prevent theft if database is compromised
    - Tokens have strictly defined expiration times
    - Linked to specific user accounts

Usage:
    token = RefreshToken(
        user_id=user.id,
        refresh_token_hash=get_token_hash("raw_token_string"),
        expires_at=datetime.utcnow() + timedelta(days=7)
    )
    db.add(token)
"""

from sqlalchemy import Column, String, DateTime, ForeignKey
from datetime import datetime
from .base import BaseModel


class RefreshToken(BaseModel):
    """
    Refresh Token model for JWT refresh flow.
    
    Attributes:
        user_id (str): ID of the user who owns this token
        refresh_token_hash (str): Secure hash of the refresh token
        expires_at (datetime): Timestamp when this token becomes invalid
    """
    
    __tablename__ = "refresh_tokens"
    
    # ========================================================================
    # TOKEN DETAILS
    # ========================================================================
    
    user_id = Column(
        String(36), 
        ForeignKey("users.id"), 
        nullable=False, 
        index=True
    )
    """
    ID of the associated user.
    Foreign key to users table. Indexed for fast lookup by user.
    """
    
    refresh_token_hash = Column(
        String(500), 
        nullable=False, 
        unique=True
    )
    """
    Hash of the actual refresh token string.
    
    We store the hash, not the token itself, so that if the database is
    compromised, valid tokens cannot be forged.
    """
    
    expires_at = Column(
        DateTime, 
        nullable=False
    )
    """
    Expiration timestamp.
    
    After this time, the token is considered invalid and cannot be used
    to generate new access tokens.
    """
    
    # ========================================================================
    # HELPER METHODS
    # ========================================================================
    
    def is_expired(self) -> bool:
        """
        Check if the token has expired.
        
        Returns:
            bool: True if current UTC time is past expires_at, False otherwise.
        """
        return datetime.utcnow() > self.expires_at
