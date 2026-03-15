"""
Experience API Endpoints
=======================

This module defines endpoints for managing work experience records.
Authentication is required for all write operations.

Features:
    - List all experience records (Public)
    - Create new experience entry (Admin)
    - Update existing entry (Admin)
    - Soft delete entry (Admin)
    - Upload company logo (Admin)

Routes:
    - GET /: List experience
    - POST /: Create experience
    - PATCH /{id}: Update experience
    - DELETE /{id}: Delete experience
    - POST /{id}/upload-logo: Upload logo
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from ...database import get_db
from ...models.experience import Experience
from ...schemas.common import StandardResponse
from ...core.deps import get_current_admin_user
from ...services.file_service import save_upload_file
from ...services.sanitize_service import sanitize_html

router = APIRouter()


# ============================================================================
# SCHEMAS
# ============================================================================

class ExperienceCreate(BaseModel):
    """Schema for creating a new experience entry."""
    company: str
    position: str
    location: Optional[str] = None
    employment_type: Optional[str] = None
    start_month_year: str
    end_month_year: Optional[str] = None
    description: Optional[str] = None


class ExperienceUpdate(BaseModel):
    """Schema for updating an experience entry (partial updates)."""
    company: Optional[str] = None
    position: Optional[str] = None
    location: Optional[str] = None
    employment_type: Optional[str] = None
    start_month_year: Optional[str] = None
    end_month_year: Optional[str] = None
    description: Optional[str] = None


class ExperienceResponse(BaseModel):
    """Schema for experience response."""
    id: str
    company: str
    position: str
    location: Optional[str]
    employment_type: Optional[str]
    start_month_year: str
    end_month_year: Optional[str]
    description: Optional[str]
    logo: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================================
# READ OPERATIONS (Public)
# ============================================================================

@router.get("", response_model=StandardResponse)
async def list_experience(db: Session = Depends(get_db)):
    """
    List all active experience records (Public).
    
    Returns a list of experience entries ordered by start date (descending).
    """
    experience_list = db.query(Experience).filter(
        Experience.is_deleted == False
    ).order_by(Experience.start_month_year.desc()).all()
    
    return StandardResponse(
        success=True,
        message=f"Retrieved {len(experience_list)} experience records",
        data=[ExperienceResponse.from_orm(exp) for exp in experience_list]
    )


# ============================================================================
# CREATE OPERATIONS (Admin Only)
# ============================================================================

@router.post("", response_model=StandardResponse)
async def create_experience(
    experience_data: ExperienceCreate,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin_user)
):
    """
    Create a new experience entry (Admin only).
    """
    payload = experience_data.dict()
    if payload.get("description"):
        payload["description"] = sanitize_html(payload["description"])

    experience = Experience(**payload)
    db.add(experience)
    db.commit()
    db.refresh(experience)
    
    return StandardResponse(
        success=True,
        message="Experience created successfully",
        data=ExperienceResponse.from_orm(experience)
    )


# ============================================================================
# UPDATE OPERATIONS (Admin Only)
# ============================================================================

@router.patch("/{experience_id}", response_model=StandardResponse)
async def update_experience(
    experience_id: str,
    updates: ExperienceUpdate,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin_user)
):
    """
    Update an experience entry (Admin only).
    """
    experience = db.query(Experience).filter(
        Experience.id == experience_id,
        Experience.is_deleted == False
    ).first()
    
    if not experience:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experience not found"
        )
    
    update_data = updates.dict(exclude_unset=True)
    if "description" in update_data and update_data["description"] is not None:
        update_data["description"] = sanitize_html(update_data["description"])
    for field, value in update_data.items():
        setattr(experience, field, value)
    
    db.commit()
    db.refresh(experience)
    
    return StandardResponse(
        success=True,
        message="Experience updated successfully",
        data=ExperienceResponse.from_orm(experience)
    )


# ============================================================================
# DELETE OPERATIONS (Admin Only)
# ============================================================================

@router.delete("/{experience_id}", response_model=StandardResponse)
async def delete_experience(
    experience_id: str,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin_user)
):
    """
    Soft delete an experience entry (Admin only).
    """
    experience = db.query(Experience).filter(
        Experience.id == experience_id,
        Experience.is_deleted == False
    ).first()
    
    if not experience:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experience not found"
        )
    
    experience.is_deleted = True
    db.commit()
    
    return StandardResponse(
        success=True,
        message="Experience deleted successfully",
        data=None
    )


# ============================================================================
# FILE UPLOADS (Admin Only)
# ============================================================================

@router.post("/{experience_id}/upload-logo", response_model=StandardResponse)
async def upload_experience_logo(
    experience_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin_user)
):
    """
    Upload company logo (Admin only).
    """
    experience = db.query(Experience).filter(
        Experience.id == experience_id,
        Experience.is_deleted == False
    ).first()
    
    if not experience:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experience not found"
        )
    
    file_path = await save_upload_file(file, db, is_image=True)
    experience.logo = file_path
    db.commit()
    
    return StandardResponse(
        success=True,
        message="Logo uploaded successfully",
        data={"file_path": file_path}
    )
