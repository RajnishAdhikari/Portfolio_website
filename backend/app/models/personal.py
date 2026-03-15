"""
Personal Information Model
=========================

This module defines the Personal model for storing user's personal/contact information.

This is typically a singleton - only one record should exist representing the portfolio owner.
Contains contact details, social media links, and file paths for profile picture and CV.

Features:
    - Contact information (name, email, phone, address)
    - Social media links (GitHub, LinkedIn, Twitter)
    - File storage paths for profile picture and CV
    - All fields are optional to allow incremental updates

Usage:
    # Get or create personal info
    personal = db.query(Personal).first()
    if not personal:
        personal = Personal()
        db.add(personal)
    
    personal.full_name = "John Doe"
    personal.email = "john@example.com"
    db.commit()
"""

from sqlalchemy import Column, String, Text
from .base import BaseModel


class Personal(BaseModel):
    """
    Personal information model for portfolio owner's details.
    
    Singleton model - should only have one active record in the database.
    Stores contact information, social links, and file paths.
    
    Attributes:
        full_name (str): Portfolio owner's full name
        tagline (str): Professional tagline/headline
        email (str): Contact email address
        phone (str): Contact phone number
        address (str): Physical address or location
        github_url (str): GitHub profile URL
        linkedin_url (str): LinkedIn profile URL
        twitter_url (str): Twitter/X profile URL
        profile_pic (str): File path to profile picture image
        cv_file (str): File path to downloadable CV/resume PDF
        
    Example:
        personal = Personal(
            full_name="Jane Developer",
            tagline="Full Stack Engineer",
            email="jane@example.com",
            github_url="https://github.com/janedeveloper"
        )
    """
    
    __tablename__ = "personal"
    
    # ========================================================================
    # BASIC INFORMATION
    # ========================================================================
    
    full_name = Column(String(255), nullable=True)
    """Portfolio owner's full name (e.g., "John Doe")"""
    
    tagline = Column(String(500))
    """
    Professional tagline or headline.
    
    Example: "Full Stack Developer | React & Python Specialist"
    Max 500 characters for a concise professional summary.
    """
    
    # ========================================================================
    # CONTACT INFORMATION
    # ========================================================================
    
    email = Column(String(255), nullable=True)
    """
    Contact email address for professional inquiries.
    
    Note: Should be publicly visible contact email, not authentication email.
    """
    
    phone = Column(String(50))
    """
    Contact phone number.
    
    Stored as string to support international formats (e.g., "+1-234-567-8900").
    Max 50 characters to accommodate various formats.
    """
    
    address = Column(Text)
    """
    Physical address or location.
    
    Can be as detailed or vague as preferred:
    - Full address: "123 Main St, City, Country 12345"
    - City only: "San Francisco, CA"
    - Remote: "Remote / Worldwide"
    """
    
    # ========================================================================
    # SOCIAL MEDIA LINKS
    # ========================================================================
    
    github_url = Column(String(500))
    """
    GitHub profile URL.
    
    Example: "https://github.com/username"
    Used to showcase code portfolio and contributions.
    """
    
    linkedin_url = Column(String(500))
    """
    LinkedIn profile URL.
    
    Example: "https://linkedin.com/in/username"
    Professional networking profile.
    """
    
    twitter_url = Column(String(500))
    """
    Twitter/X profile URL.
    
    Example: "https://twitter.com/username"
    Social media presence for professional updates.
    """
    
    # ========================================================================
    # FILE PATHS
    # ========================================================================
    
    profile_pic = Column(String(500))
    """
    File path to profile picture image.
    
    Relative path within uploads directory (e.g., "profile_pics/photo.jpg").
    Frontend will construct full URL as: /uploads/{profile_pic}
    Recommended: Square image, at least 400x400px, JPG or PNG.
    """
    
    cv_file = Column(String(500))
    """
    File path to CV/resume PDF for download.
    
    Relative path within uploads directory (e.g., "cv/resume.pdf").
    Frontend will construct download link as: /uploads/{cv_file}
    Should be a PDF file for universal compatibility.
    """
