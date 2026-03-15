"""
Education API Endpoints
======================

This module defines endpoints for managing education records.
Authentication is required for all write operations.

Features:
    - List all education records (Public)
    - Create new education entry (Admin)
    - Update existing entry (Admin)
    - Soft delete entry (Admin)
    - Upload institution logo (Admin)

Routes:
    - GET /: List education
    - POST /: Create education
    - PATCH /{id}: Update education
    - DELETE /{id}: Delete education
    - POST /{id}/upload-logo: Upload logo
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from ...database import get_db
from ...models.education import Education
from ...schemas.common import StandardResponse
from ...core.deps import get_current_admin_user
from ...services.file_service import save_upload_file
from ...services.sanitize_service import sanitize_html

router = APIRouter()


# ============================================================================
# SCHEMAS
# ============================================================================

class EducationCreate(BaseModel):
    """Schema for creating a new education entry."""
    institution: str
    degree: str
    field: Optional[str] = None
    location: Optional[str] = None
    grade: Optional[str] = None
    start_month_year: str
    end_month_year: Optional[str] = None
    description: Optional[str] = None


class EducationUpdate(BaseModel):
    """Schema for updating an education entry (partial updates)."""
    institution: Optional[str] = None
    degree: Optional[str] = None
    field: Optional[str] = None
    location: Optional[str] = None
    grade: Optional[str] = None
    start_month_year: Optional[str] = None
    end_month_year: Optional[str] = None
    description: Optional[str] = None


class EducationResponse(BaseModel):
    """Schema for education response."""
    id: str
    institution: str
    degree: str
    field: Optional[str]
    location: Optional[str]
    grade: Optional[str]
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
async def list_education(db: Session = Depends(get_db)):
    """
    List all active education records (Public).
    
    Returns a list of education entries ordered by start date (descending).
    """
    education_list = db.query(Education).filter(
        Education.is_deleted == False
    ).order_by(Education.start_month_year.desc()).all()
    
    return StandardResponse(
        success=True,
        message=f"Retrieved {len(education_list)} education records",
        data=[EducationResponse.from_orm(edu) for edu in education_list]
    )


# ============================================================================
# CREATE OPERATIONS (Admin Only)
# ============================================================================

@router.post("", response_model=StandardResponse)
async def create_education(
    education_data: EducationCreate,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin_user)
):
    """
    Create a new education entry (Admin only).
    """
    payload = education_data.dict()
    if payload.get("description"):
        payload["description"] = sanitize_html(payload["description"])

    education = Education(**payload)
    db.add(education)
    db.commit()
    db.refresh(education)
    
    return StandardResponse(
        success=True,
        message="Education created successfully",
        data=EducationResponse.from_orm(education)
    )


# ============================================================================
# UPDATE OPERATIONS (Admin Only)
# ============================================================================

@router.patch("/{education_id}", response_model=StandardResponse)
async def update_education(
    education_id: str,
    updates: EducationUpdate,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin_user)
):
    """
    Update an education entry (Admin only).
    
    Partially updates the specified fields.
    """
    education = db.query(Education).filter(
        Education.id == education_id,
        Education.is_deleted == False
    ).first()
    
    if not education:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Education not found"
        )
    
    update_data = updates.dict(exclude_unset=True)
    if "description" in update_data and update_data["description"] is not None:
        update_data["description"] = sanitize_html(update_data["description"])
    for field, value in update_data.items():
        setattr(education, field, value)
    
    db.commit()
    db.refresh(education)
    
    return StandardResponse(
        success=True,
        message="Education updated successfully",
        data=EducationResponse.from_orm(education)
    )


# ============================================================================
# DELETE OPERATIONS (Admin Only)
# ============================================================================

@router.delete("/{education_id}", response_model=StandardResponse)
async def delete_education(
    education_id: str,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin_user)
):
    """
    Soft delete an education entry (Admin only).
    """
    education = db.query(Education).filter(
        Education.id == education_id,
        Education.is_deleted == False
    ).first()
    
    if not education:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Education not found"
        )
    
    education.is_deleted = True
    db.commit()
    
    return StandardResponse(
        success=True,
        message="Education deleted successfully",
        data=None
    )


# ============================================================================
# FILE UPLOADS (Admin Only)
# ============================================================================

@router.post("/{education_id}/upload-logo", response_model=StandardResponse)
async def upload_education_logo(
    education_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin_user)
):
    """
    Upload institution logo (Admin only).
    """
    education = db.query(Education).filter(
        Education.id == education_id,
        Education.is_deleted == False
    ).first()
    
    if not education:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Education not found"
        )
    
    file_path = await save_upload_file(file, db, is_image=True)
    education.logo = file_path
    db.commit()
    
    return StandardResponse(
        success=True,
        message="Logo uploaded successfully",
        data={"file_path": file_path}
    )
