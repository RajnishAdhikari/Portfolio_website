"""
Resource Paper Model
===================

This module defines the ResourcePaper model, which functions similarly to Articles
but is distinct for showcasing research papers, white papers, or academic resources.

Features:
    - Separation from blog articles
    - Research-focused fields
    - PDF-centric content sharing

Usage:
    paper = ResourcePaper(
        title="AI Research 2023",
        slug="ai-research-2023",
        excerpt="Abstract of the paper..."
    )
    db.add(paper)
"""

from sqlalchemy import Column, String, Text, Boolean
from .base import BaseModel


class ResourcePaper(BaseModel):
    """
    Resource Paper model for academic or technical papers.
    
    Often used for items where the PDF attachment is the primary content,
    while the body provides an abstract or summary.
    
    Attributes:
        title (str): Paper title
        slug (str): Unique URL identifier
        excerpt (str): Abstract or brief summary
        body (str): Full text or detailed abstract
        cover_image (str): Thumbnail or paper preview image
        pdf_attachment (str): The paper file itself
        external_url (str): DOI link or publisher URL
        is_featured (bool): Highlight flag
    """
    
    __tablename__ = "resource_papers"
    
    # ========================================================================
    # CONTENT
    # ========================================================================
    
    title = Column(String(255), nullable=False)
    """Paper title (required)."""
    
    slug = Column(
        String(255), 
        unique=True, 
        nullable=False, 
        index=True
    )
    """URL-friendly identifier."""
    
    excerpt = Column(String(200), nullable=False)
    """Abstract summary or brief description."""
    
    body = Column(Text)
    """Detailed abstract or full content."""
    
    # ========================================================================
    # MEDIA & FILES
    # ========================================================================
    
    cover_image = Column(String(500), nullable=True)
    """Preview image path."""
    
    pdf_attachment = Column(String(500))
    """Path to the PDF document file."""
    
    external_url = Column(String(500))
    """External link (DOI, Publisher, etc.)."""
    
    # ========================================================================
    # METADATA
    # ========================================================================
    
    is_featured = Column(
        Boolean, 
        default=False, 
        nullable=False
    )
    """Flag to highlight important papers."""
