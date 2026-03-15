"""
Skill Model
==========

This module defines the Skill model for tracking technical proficiencies.
Skills are categorized and rated by proficiency level.

Features:
    - Categorized skills (Frontend, Backend, etc.)
    - Proficiency rating (1-5)
    - Enum-based strict categorization

Usage:
    skill = Skill(
        name="Python",
        category=SkillCategory.BACKEND,
        level=5
    )
    db.add(skill)
"""

from sqlalchemy import Column, String, Integer, Enum
from .base import BaseModel
import enum


# ============================================================================
# SKILL CATEGORIES
# ============================================================================

class SkillCategory(str, enum.Enum):
    """
    Enumeration of skill categories for better organization.
    """
    FRONTEND = "Frontend"
    BACKEND = "Backend"
    LANGUAGE = "Language"
    TOOL = "Tool"
    OTHER = "Other"


# ============================================================================
# SKILL MODEL
# ============================================================================

class Skill(BaseModel):
    """
    Skill model representing a technical ability or tool proficiency.
    
    Attributes:
        category (SkillCategory): The category the skill belongs to
        name (str): Name of the skill (e.g., "React", "Python")
        level (int): Proficiency level from 1 to 5
    """
    
    __tablename__ = "skills"
    
    # ========================================================================
    # SKILL DETAILS
    # ========================================================================
    
    category = Column(Enum(SkillCategory), nullable=False, index=True)
    """Category of the skill. Indexed for filtering."""
    
    name = Column(String(255), nullable=False)
    """Name of the skill or technology (required)."""
    
    level = Column(Integer, nullable=False)
    """
    Proficiency level:
    1 - Beginner
    2 - Elementary
    3 - Intermediate
    4 - Advanced
    5 - Expert
    """
