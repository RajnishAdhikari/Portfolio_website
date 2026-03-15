"""
Skills API Endpoints
===================

This module defines endpoints for managing technical skills.
Skills can be categorized and rated by proficiency level.

Features:
    - List all skills grouped by category (Public)
    - Create new skill (Admin)
    - Update existing skill (Admin)
    - Soft delete skill (Admin)

Routes:
    - GET /: List skills
    - POST /: Create skill
    - PATCH /{id}: Update skill
    - DELETE /{id}: Delete skill
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, conint
from datetime import datetime

from ...database import get_db
from ...models.skill import Skill
from ...schemas.common import StandardResponse
from ...core.deps import get_current_admin_user

router = APIRouter()


# ============================================================================
# SCHEMAS
# ============================================================================

class SkillCreate(BaseModel):
    """Schema for creating a new skill."""
    category: str
    name: str
    level: conint(ge=1, le=5)  # Constrained integer 1-5


class SkillUpdate(BaseModel):
    """Schema for updating a skill (partial updates)."""
    category: Optional[str] = None
    name: Optional[str] = None
    level: Optional[conint(ge=1, le=5)] = None


class SkillResponse(BaseModel):
    """Schema for skill response."""
    id: str
    category: str
    name: str
    level: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================================
# READ OPERATIONS (Public)
# ============================================================================

@router.get("", response_model=StandardResponse)
async def list_skills(
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    List all active skills (Public).
    Optionally filter by category.
    """
    query = db.query(Skill).filter(Skill.is_deleted == False)
    
    if category:
        query = query.filter(Skill.category == category)
    
    skills = query.order_by(Skill.category, Skill.level.desc()).all()
    
    return StandardResponse(
        success=True,
        message=f"Retrieved {len(skills)} skills",
        data=[SkillResponse.from_orm(s) for s in skills]
    )


# ============================================================================
# CREATE OPERATIONS (Admin Only)
# ============================================================================

@router.post("", response_model=StandardResponse)
async def create_skill(
    skill_data: SkillCreate,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin_user)
):
    """
    Create a new skill (Admin only).
    """
    skill = Skill(**skill_data.dict())
    db.add(skill)
    db.commit()
    db.refresh(skill)
    
    return StandardResponse(
        success=True,
        message="Skill created successfully",
        data=SkillResponse.from_orm(skill)
    )


# ============================================================================
# UPDATE OPERATIONS (Admin Only)
# ============================================================================

@router.patch("/{skill_id}", response_model=StandardResponse)
async def update_skill(
    skill_id: str,
    updates: SkillUpdate,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin_user)
):
    """
    Update a skill (Admin only).
    """
    skill = db.query(Skill).filter(
        Skill.id == skill_id,
        Skill.is_deleted == False
    ).first()
    
    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found"
        )
    
    update_data = updates.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(skill, field, value)
    
    db.commit()
    db.refresh(skill)
    
    return StandardResponse(
        success=True,
        message="Skill updated successfully",
        data=SkillResponse.from_orm(skill)
    )


# ============================================================================
# DELETE OPERATIONS (Admin Only)
# ============================================================================

@router.delete("/{skill_id}", response_model=StandardResponse)
async def delete_skill(
    skill_id: str,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin_user)
):
    """
    Soft delete a skill (Admin only).
    """
    skill = db.query(Skill).filter(
        Skill.id == skill_id,
        Skill.is_deleted == False
    ).first()
    
    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found"
        )
    
    skill.is_deleted = True
    db.commit()
    
    return StandardResponse(
        success=True,
        message="Skill deleted successfully",
        data=None
    )
