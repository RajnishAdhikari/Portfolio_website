"""
Authentication Schemas
=====================

Pydantic models for authentication data transfer objects.
"""

from typing import Optional
from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    """
    Schema for user login credentials.
    """
    email: EmailStr
    password: str


class Token(BaseModel):
    """
    Schema for JWT token response.
    """
    access_token: str
    token_type: str
    refresh_token: Optional[str] = None


class TokenData(BaseModel):
    """
    Schema for data embedded in JWT token.
    """
    sub: Optional[str] = None
    role: Optional[str] = None


class RegisterRequest(BaseModel):
    """
    Schema for user registration (Admin use).
    """
    email: EmailStr
    password: str
    role: Optional[str] = "contributor"
