"""
Education Model
==============

This module defines the Education model for storing academic background.
Details can include degree, field of study, institution, grades, and dates.

Features:
    - Academic history tracking
    - Degree and field specifications
    - Grade/GPA storage
    - Logo support for institutions

Usage:
    education = Education(
        institution="University of Tech",
        degree="B.Sc.",
        field="Computer Science",
        start_month_year="2018-09"
    )
    db.add(education)
"""

from sqlalchemy import Column, String, Text
from .base import BaseModel


class Education(BaseModel):
    """
    Education model representing an academic achievement or period of study.
    
    Attributes:
        institution (str): Name of university, school, or organization
        degree (str): Degree obtained (e.g., "Bachelor of Science")
        field (str): Field of study (e.g., "Computer Science")
        location (str): City/Country of the institution
        grade (str): GPA or grade achieved
        start_month_year (str): Start date (YYYY-MM)
        end_month_year (str): End date (YYYY-MM), null if ongoing
        description (str): Detailed description or JSON content (TipTap)
        logo (str): Path to institution logo image file
    """
    
    __tablename__ = "education"
    
    # ========================================================================
    # INSTITUTION DETAILS
    # ========================================================================
    
    institution = Column(String(255), nullable=False)
    """Name of the educational institution (required)."""
    
    degree = Column(String(255), nullable=False)
    """Degree or certification name (required)."""
    
    field = Column(String(255))
    """Field of study or major."""
    
    location = Column(String(255))
    """Physical location of the institution."""
    
    # ========================================================================
    # PERFORMANCE & TIMELINE
    # ========================================================================
    
    grade = Column(String(50))
    """Grade, GPA, or classification achieved."""
    
    start_month_year = Column(String(20), nullable=False)
    """Start date in YYYY-MM format (required)."""
    
    end_month_year = Column(String(20))
    """End date in YYYY-MM format. Null indicates currently studying."""
    
    # ========================================================================
    # ADDITIONAL CONTENT
    # ========================================================================
    
    description = Column(Text)
    """Detailed description, coursework, or achievements. Can store HTML or JSON."""
    
    logo = Column(String(500))
    """File path to the institution's logo image."""
