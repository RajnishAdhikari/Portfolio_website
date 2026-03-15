"""
Article Model
============

This module defines the Article model for the blog/articles section.
Supports publishing written content with SEO features and media support.

Features:
    - Blog post management
    - Slug-based routing
    - Featured article flagging
    - Rich text content
    - File attachments

Usage:
    article = Article(
        title="Getting Started with FastAPI",
        slug="getting-started-fastapi",
        excerpt="A quick guide to FastAPI...",
        is_featured=True
    )
    db.add(article)
"""

from sqlalchemy import Column, String, Text, Boolean
from .base import BaseModel


class Article(BaseModel):
    """
    Article model representing a blog post or technical article.
    
    Attributes:
        title (str): Article headline
        slug (str): Unique URL identifier
        excerpt (str): Short summary for listings
        body (str): Full article content (TipTap JSON/HTML)
        cover_image (str): Header image path
        pdf_attachment (str): Associated PDF path
        external_url (str): Link to original/external publication
        is_featured (bool): Flag to highlight important articles
    """
    
    __tablename__ = "articles"
    
    # ========================================================================
    # CONTENT
    # ========================================================================
    
    title = Column(String(255), nullable=False)
    """Article headline/title (required)."""
    
    slug = Column(
        String(255), 
        unique=True,      # Must be unique
        nullable=False,   # Required
        index=True        # Indexed for lookups
    )
    """URL-friendly identifier for routing."""
    
    excerpt = Column(String(200), nullable=False)
    """
    Brief summary or intro preview.
    Shown in article lists and used for meta description.
    """
    
    body = Column(Text)
    """Full article body content (HTML or JSON)."""
    
    # ========================================================================
    # MEDIA & LINKS
    # ========================================================================
    
    cover_image = Column(String(500), nullable=True)
    """Path to article cover/header image."""
    
    pdf_attachment = Column(String(500))
    """Path to downloadable PDF version or attachment."""
    
    external_url = Column(String(500))
    """
    Link to original publication if republished.
    e.g., Medium link, Dev.to link
    """
    
    # ========================================================================
    # METADATA
    # ========================================================================
    
    is_featured = Column(
        Boolean, 
        default=False,    # Defaults to standard article
        nullable=False
    )
    """Flag to pin article to top or show in featured section."""
