"""
Certification Model
==================

This module defines the Certification model for professional credentials.
Stores details about certificates, licenses, and awards.

Features:
    - Credential tracking
    - Verification links
    - Image support for certificates

Usage:
    cert = Certification(
        name="AWS Certified Developer",
        issuer="Amazon Web Services",
        issue_month_year="2023-01",
        cred_id="AWS-DEC-12345"
    )
    db.add(cert)
"""

from sqlalchemy import Column, String, Text
from .base import BaseModel


class Certification(BaseModel):
    """
    Certification model representing a professional qualification.
    
    Attributes:
        name (str): Name of the certification
        issuer (str): Organization that issued the certificate
        issue_month_year (str): Date of issue (YYYY-MM)
        cred_id (str): Credential ID or verification code
        cred_url (str): URL to verify the credential online
        description (str): Details about what was earned
        image (str): Path to certificate image/scan
    """
    
    __tablename__ = "certifications"
    
    # ========================================================================
    # CREDENTIAL DETAILS
    # ========================================================================
    
    name = Column(String(255), nullable=False)
    """Name of the certification or award (required)."""
    
    issuer = Column(String(255), nullable=False)
    """Issuing organization or body (required)."""
    
    issue_month_year = Column(String(20), nullable=False)
    """Date issued in YYYY-MM format (required)."""
    
    # ========================================================================
    # VERIFICATION
    # ========================================================================
    
    cred_id = Column(String(255))
    """Credential ID or license number for verification."""
    
    cred_url = Column(String(500))
    """URL to verify the credential online."""
    
    # ========================================================================
    # CONTENT
    # ========================================================================
    
    description = Column(Text)
    """Description of the certification, skills validated, etc."""
    
    image = Column(String(500), nullable=True)
    """File path to an image or scan of the certificate."""
