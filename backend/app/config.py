"""
Application Configuration Management
===================================

This module manages all application settings using Pydantic Settings.
Configuration values are loaded from environment variables and the .env file.

Key Features:
    - Environment-based configuration (dev, staging, production)
    - Type-safe settings with validation
    - Cached settings instance for performance
    - Convenient utility properties for common conversions

Environment Variables (.env file):
    ENVIRONMENT: dev|staging|production
    DATABASE_URL: SQLAlchemy database connection string
    SECRET_KEY: JWT signing secret key (keep secure!)
    ALGORITHM: JWT algorithm (default: HS256)
    ACCESS_TOKEN_EXPIRE_MINUTES: JWT access token lifetime
    REFRESH_TOKEN_EXPIRE_DAYS: JWT refresh token lifetime
    CORS_ORIGINS: Comma-separated allowed origins
    MAX_IMAGE_SIZE_MB: Maximum image upload size in MB
    MAX_PDF_SIZE_MB: Maximum PDF upload size in MB
    UPLOAD_DIR: Directory for file uploads
    RATE_LIMIT_PER_MINUTE: API rate limit per minute
    HOST: Server host address
    PORT: Server port number

Usage:
    from app.config import get_settings
    
    settings = get_settings()
    print(settings.database_url)
"""

from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache


class Settings(BaseSettings):
    """
    Application settings with environment-based configuration.
    
    All settings can be overridden via environment variables or .env file.
    Pydantic validates types and provides intelligent defaults.
    """
    
    # ========================================================================
    # ENVIRONMENT CONFIGURATION
    # ========================================================================
    
    environment: str = "dev"
    """Application environment: dev, staging, or production"""
    
    # ========================================================================
    # DATABASE CONFIGURATION
    # ========================================================================
    
    database_url: str
    """
    SQLAlchemy database connection string.
    
    Examples:
        SQLite: "sqlite:///./app.db"
        PostgreSQL: "postgresql://user:pass@localhost/dbname"
        MySQL: "mysql+pymysql://user:pass@localhost/dbname"
    
    Required: Must be provided via environment variable
    """
    
    # ========================================================================
    # JWT AUTHENTICATION CONFIGURATION
    # ========================================================================
    
    secret_key: str
    """
    Secret key for JWT token signing.
    
    Security: Keep this secret! Never commit to version control.
    Generate with: openssl rand -hex 32
    Required: Must be provided via environment variable
    """
    
    algorithm: str = "HS256"
    """JWT signing algorithm (default: HS256)"""
    
    access_token_expire_minutes: int = 30
    """Access token lifetime in minutes (default: 30)"""
    
    refresh_token_expire_days: int = 7
    """Refresh token lifetime in days (default: 7)"""
    
    # ========================================================================
    # CORS CONFIGURATION
    # ========================================================================
    
    cors_origins: str = "http://localhost:5173"
    """
    Allowed CORS origins (comma-separated for multiple).
    
    Example: "http://localhost:3000,https://myapp.com"
    Default: "http://localhost:5173" (Vite dev server)
    """
    
    # ========================================================================
    # FILE UPLOAD CONFIGURATION
    # ========================================================================
    
    max_image_size_mb: int = 5
    """Maximum allowed image upload size in megabytes (default: 5MB)"""
    
    max_pdf_size_mb: int = 10
    """Maximum allowed PDF upload size in megabytes (default: 10MB)"""
    
    upload_dir: str = "uploads"
    """Directory path for storing uploaded files (default: "uploads")"""
    
    # ========================================================================
    # RATE LIMITING CONFIGURATION
    # ========================================================================
    
    rate_limit_per_minute: int = 100
    """Maximum API requests per minute per IP (default: 100)"""

    auto_create_tables: bool = False
    """Create missing database tables on startup when enabled"""
    
    # ========================================================================
    # SERVER CONFIGURATION
    # ========================================================================
    
    host: str = "0.0.0.0"
    """Server host address (default: 0.0.0.0 for all interfaces)"""
    
    port: int = 8000
    """Server port number (default: 8000)"""
    
    # ========================================================================
    # UTILITY PROPERTIES
    # ========================================================================
    
    @property
    def cors_origins_list(self) -> List[str]:
        """
        Convert CORS origins string to list for middleware.
        
        Returns:
            List[str]: List of allowed origin URLs
            
        Example:
            "http://localhost:3000,https://app.com" -> 
            ["http://localhost:3000", "https://app.com"]
        """
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    @property
    def max_image_size_bytes(self) -> int:
        """
        Convert max image size from MB to bytes.
        
        Returns:
            int: Maximum image size in bytes
        """
        return self.max_image_size_mb * 1024 * 1024
    
    @property
    def max_pdf_size_bytes(self) -> int:
        """
        Convert max PDF size from MB to bytes.
        
        Returns:
            int: Maximum PDF size in bytes
        """
        return self.max_pdf_size_mb * 1024 * 1024
    
    class Config:
        """Pydantic configuration"""
        env_file = ".env"           # Load variables from .env file
        case_sensitive = False      # Environment variables are case-insensitive


# ============================================================================
# SETTINGS FACTORY
# ============================================================================

@lru_cache()
def get_settings() -> Settings:
    """
    Get cached application settings instance.
    
    Uses LRU cache to ensure settings are only loaded once,
    improving performance by avoiding repeated file reads.
    
    Returns:
        Settings: Cached settings instance
        
    Usage:
        settings = get_settings()
        print(settings.database_url)
    """
    return Settings()
