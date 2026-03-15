"""
Extracurricular Activity Model
=============================

This module defines the Extracurricular model for activities outside of work/education.
Includes volunteering, hobbies, awards, and community service.

Features:
    - Volunteer work tracking
    - Achievement showcasing
    - Certificate image support

Usage:
    activity = Extracurricular(
        title="Volunteer Mentor",
        organisation="Code for Good",
        start_month_year="2022-01"
    )
    db.add(activity)
"""

from sqlalchemy import Column, String, Text
from .base import BaseModel


class Extracurricular(BaseModel):
    """
    Extracurricular model for hobbies, volunteering, or other activities.
    
    Attributes:
        title (str): Role or Activity name
        organisation (str): Organization name
        start_month_year (str): Start date (YYYY-MM)
        end_month_year (str): End date (YYYY-MM)
        description (str): Details about the activity
        certificate_image (str): Path to image/certificate
        external_url (str): Link to organization or event
    """
    
    __tablename__ = "extracurricular"
    
    # ========================================================================
    # ACTIVITY DETAILS
    # ========================================================================
    
    title = Column(String(255), nullable=False)
    """Role title or activity name (required)."""
    
    organisation = Column(String(255))
    """Organization name (mutable/optional)."""
    
    # ========================================================================
    # TIMELINE
    # ========================================================================
    
    start_month_year = Column(String(20))
    """Start date in YYYY-MM format."""
    
    end_month_year = Column(String(20))
    """End date in YYYY-MM format. Null if ongoing."""
    
    # ========================================================================
    # CONTENT
    # ========================================================================
    
    description = Column(Text)
    """Detailed description of the activity and contributions."""
    
    certificate_image = Column(String(500))
    """File path to associated certificate or photo."""
    
    external_url = Column(String(500))
    """External link to organization or project."""
