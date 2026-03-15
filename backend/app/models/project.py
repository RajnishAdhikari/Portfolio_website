"""
Project Model
============

This module defines the Project model for showcasing portfolio work.
Projects are the core content of the portfolio, featuring rich descriptions,
tech stacks, and multiple media attachments.

Features:
    - URL-friendly slugs for routing
    - Rich text content support
    - JSON storage for tech stack and image galleries
    - External link integration (GitHub, live demo)
    - PDF attachment support (case studies)

Usage:
    project = Project(
        title="Portfolio Site",
        slug="portfolio-site",
        short_desc="My personal portfolio",
        tech_stack=["React", "FastAPI"],
        github_url="https://github.com/me/portfolio"
    )
    db.add(project)
"""

from sqlalchemy import Column, String, Text, JSON
from .base import BaseModel


class Project(BaseModel):
    """
    Project model representing a portfolio item.
    
    Attributes:
        title (str): Project display title
        slug (str): Unique URL-friendly identifier
        short_desc (str): Brief summary for cards/lists
        detailed_desc (str): Rich text/JSON content
        cover_image (str): Main thumbnail image path
        images (list): JSON array of gallery image paths
        pdf_attachment (str): Path to associated PDF file
        external_url (str): Link to live demo/website
        github_url (str): Link to source code
        tech_stack (list): JSON array of technology names
    """
    
    __tablename__ = "projects"
    
    # ========================================================================
    # BASIC INFORMATION
    # ========================================================================
    
    title = Column(String(255), nullable=False)
    """Project title (required)."""
    
    slug = Column(
        String(255), 
        unique=True,      # Must be unique for URLs
        nullable=False,   # Required
        index=True        # Indexed for fast lookups
    )
    """
    URL-friendly slug identifier.
    
    Example: "my-awesome-project"
    Must be unique across all projects. Used in routing: /projects/{slug}
    """
    
    # ========================================================================
    # CONTENT
    # ========================================================================
    
    short_desc = Column(String(160), nullable=False)
    """
    Brief summary for project cards and SEO meta descriptions.
    Restricted to 160 characters for optimal display.
    """
    
    detailed_desc = Column(Text)
    """
    Full project description.
    
    Can store rich text content (HTML) or structured JSON from editors like TipTap.
    """
    
    tech_stack = Column(JSON)
    """
    List of technologies used.
    
    Stored as JSON array of strings.
    Example: ["Python", "FastAPI", "React", "Docker"]
    """
    
    # ========================================================================
    # MEDIA & FILES
    # ========================================================================
    
    cover_image = Column(String(500), nullable=True)
    """Path to the main cover image/thumbnail."""
    
    images = Column(JSON)
    """
    Additional gallery images.
    
    Stored as JSON array of file paths.
    Example: ["/uploads/p1/shot1.jpg", "/uploads/p1/shot2.jpg"]
    """
    
    pdf_attachment = Column(String(500))
    """Path to associated PDF (e.g., case study, diagrams)."""
    
    # ========================================================================
    # LINKS
    # ========================================================================
    
    external_url = Column(String(500))
    """Link to live demo or deployed application."""
    
    github_url = Column(String(500))
    """Link to GitHub repository or source code."""
