"""
Extracurricular Activity API Endpoints
=====================================

This module defines endpoints for managing extracurricular activities.
Includes hobbies, volunteering, and other non-work achievements.

Features:
    - List all activities (Public)
    - Create new activity (Admin)
    - Update existing activity (Admin)
    - Soft delete activity (Admin)
    - Upload certificate image (Admin)

Routes:
    - GET /: List activities
    - POST /: Create activity
    - PATCH /{id}: Update activity
    - DELETE /{id}: Delete activity
    - POST /{id}/upload-certificate: Upload certificate
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from ...database import get_db
from ...models.extracurricular import Extracurricular
from ...schemas.common import StandardResponse
from ...core.deps import get_current_admin_user
from ...services.file_service import save_upload_file
from ...services.sanitize_service import sanitize_html

router = APIRouter()


# ============================================================================
# SCHEMAS
# ============================================================================

class ExtracurricularCreate(BaseModel):
    """Schema for creating a new activity."""
    title: str
    organisation: Optional[str] = None
    description: Optional[str] = None
    start_month_year: Optional[str] = None
    end_month_year: Optional[str] = None
    external_url: Optional[str] = None


class ExtracurricularUpdate(BaseModel):
    """Schema for updating an activity (partial updates)."""
    title: Optional[str] = None
    organisation: Optional[str] = None
    description: Optional[str] = None
    start_month_year: Optional[str] = None
    end_month_year: Optional[str] = None
    external_url: Optional[str] = None


class ExtracurricularResponse(BaseModel):
    """Schema for activity response."""
    id: str
    title: str
    organisation: Optional[str]
    description: Optional[str]
    start_month_year: Optional[str]
    end_month_year: Optional[str]
    external_url: Optional[str]
    certificate_image: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================================
# READ OPERATIONS (Public)
# ============================================================================

@router.get("", response_model=StandardResponse)
async def list_activities(db: Session = Depends(get_db)):
    """
    List all active extracurricular activities (Public).
    
    Returns a list of activities ordered by start date (descending),
    with undated activities last.
    """
    # Sort by start date, nulls last logic handled by DB specific or Python
    # Here we do simple fetch and could enhance sorting
    activities = db.query(Extracurricular).filter(
        Extracurricular.is_deleted == False
    ).order_by(Extracurricular.start_month_year.desc()).all()
    
    return StandardResponse(
        success=True,
        message=f"Retrieved {len(activities)} activities",
        data=[ExtracurricularResponse.from_orm(a) for a in activities]
    )


# ============================================================================
# CREATE OPERATIONS (Admin Only)
# ============================================================================

@router.post("", response_model=StandardResponse)
async def create_activity(
    activity_data: ExtracurricularCreate,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin_user)
):
    """
    Create a new extracurricular activity (Admin only).
    """
    payload = activity_data.dict()
    if payload.get("description"):
        payload["description"] = sanitize_html(payload["description"])

    activity = Extracurricular(**payload)
    db.add(activity)
    db.commit()
    db.refresh(activity)
    
    return StandardResponse(
        success=True,
        message="Activity created successfully",
        data=ExtracurricularResponse.from_orm(activity)
    )


# ============================================================================
# UPDATE OPERATIONS (Admin Only)
# ============================================================================

@router.patch("/{activity_id}", response_model=StandardResponse)
async def update_activity(
    activity_id: str,
    updates: ExtracurricularUpdate,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin_user)
):
    """
    Update an activity (Admin only).
    """
    activity = db.query(Extracurricular).filter(
        Extracurricular.id == activity_id,
        Extracurricular.is_deleted == False
    ).first()
    
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    update_data = updates.dict(exclude_unset=True)
    if "description" in update_data and update_data["description"] is not None:
        update_data["description"] = sanitize_html(update_data["description"])
    for field, value in update_data.items():
        setattr(activity, field, value)
    
    db.commit()
    db.refresh(activity)
    
    return StandardResponse(
        success=True,
        message="Activity updated successfully",
        data=ExtracurricularResponse.from_orm(activity)
    )


# ============================================================================
# DELETE OPERATIONS (Admin Only)
# ============================================================================

@router.delete("/{activity_id}", response_model=StandardResponse)
async def delete_activity(
    activity_id: str,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin_user)
):
    """
    Soft delete an activity (Admin only).
    """
    activity = db.query(Extracurricular).filter(
        Extracurricular.id == activity_id,
        Extracurricular.is_deleted == False
    ).first()
    
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    activity.is_deleted = True
    db.commit()
    
    return StandardResponse(
        success=True,
        message="Activity deleted successfully",
        data=None
    )


# ============================================================================
# FILE UPLOADS (Admin Only)
# ============================================================================

@router.post("/{activity_id}/upload-certificate", response_model=StandardResponse)
async def upload_activity_certificate(
    activity_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin_user)
):
    """
    Upload actvity certificate/image (Admin only).
    """
    activity = db.query(Extracurricular).filter(
        Extracurricular.id == activity_id,
        Extracurricular.is_deleted == False
    ).first()
    
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    file_path = await save_upload_file(file, db, is_image=True)
    activity.certificate_image = file_path
    db.commit()
    
    return StandardResponse(
        success=True,
        message="Certificate uploaded successfully",
        data={"file_path": file_path}
    )
