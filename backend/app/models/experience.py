"""
Experience Model
===============

This module defines the Experience model for storing professional work history.
Includes employment details, dates, and descriptions of roles.

Features:
    - Professional history tracking
    - Employment type specification
    - Ongoing position support (null end date)
    - Company logo support

Usage:
    job = Experience(
        company="Tech Corp",
        position="Senior Developer",
        start_month_year="2020-01",
        employment_type="Full-time"
    )
    db.add(job)
"""

from sqlalchemy import Column, String, Text
from .base import BaseModel


class Experience(BaseModel):
    """
    Experience model representing a professional role or job.
    
    Attributes:
        company (str): Name of the employer
        position (str): Job title
        location (str): City/Country of employment
        employment_type (str): Type of employment (Full-time, Contract, etc.)
        start_month_year (str): Start date (YYYY-MM)
        end_month_year (str): End date (YYYY-MM), null if current job
        description (str): Detailed description or JSON content
        logo (str): Path to company logo image file
    """
    
    __tablename__ = "experience"
    
    # ========================================================================
    # COMPANY & ROLE DETAILS
    # ========================================================================
    
    company = Column(String(255), nullable=False)
    """Name of the company or organization (required)."""
    
    position = Column(String(255), nullable=False)
    """Job title or role (required)."""
    
    location = Column(String(255))
    """Physical or remote location of the job."""
    
    employment_type = Column(String(100))
    """Type of employment (e.g., Full-time, Part-time, Contract)."""
    
    # ========================================================================
    # TIMELINE
    # ========================================================================
    
    start_month_year = Column(String(20), nullable=False)
    """Start date in YYYY-MM format (required)."""
    
    end_month_year = Column(String(20))
    """End date in YYYY-MM format. Null indicates currently employed."""
    
    # ========================================================================
    # ADDITIONAL CONTENT
    # ========================================================================
    
    description = Column(Text)
    """Detailed description of responsibilities and achievements."""
    
    logo = Column(String(500))
    """File path to the company's logo image."""
