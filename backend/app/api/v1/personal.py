"""
Personal Information API Endpoints
=================================

This module defines endpoints for managing the portfolio owner's personal details.
Includes contact info, social links, profile picture, and CV upload.

Features:
    - Get public profile information
    - Update profile details (Admin only)
    - Upload profile picture (Admin only)
    - Upload CV (Admin only)

Routes:
    - GET /: Get personal info
    - PATCH /: Update personal info
    - POST /upload-profile-pic: Upload profile picture
    - POST /upload-cv: Upload CV PDF
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel, EmailStr

from ...database import get_db
from ...models.personal import Personal
from ...schemas.common import StandardResponse
from ...core.deps import get_current_admin_user
from ...services.file_service import save_upload_file

router = APIRouter()


# ============================================================================
# SCHEMAS
# ============================================================================

class PersonalUpdate(BaseModel):
    """Schema for updating personal information (partial updates allowed)."""
    full_name: Optional[str] = None
    tagline: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    twitter_url: Optional[str] = None


class PersonalResponse(BaseModel):
    """Schema for personal information response."""
    id: str
    full_name: Optional[str]
    tagline: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    address: Optional[str]
    github_url: Optional[str]
    linkedin_url: Optional[str]
    twitter_url: Optional[str]
    profile_pic: Optional[str]
    cv_file: Optional[str]
    
    class Config:
        from_attributes = True


# ============================================================================
# READ OPERATIONS (Public)
# ============================================================================

@router.get("", response_model=StandardResponse)
async def get_personal_info(db: Session = Depends(get_db)):
    """
    Get personal information (public).
    
    Returns the single Personal record containing contact details,
    social links, and file paths.
    
    Returns:
        StandardResponse with PersonalResponse data or None if not set
    """
    personal = db.query(Personal).filter(Personal.is_deleted == False).first()
    
    if not personal:
        return StandardResponse(
            success=True,
            message="No personal information found",
            data=None
        )
    
    return StandardResponse(
        success=True,
        message="Personal information retrieved successfully",
        data=PersonalResponse.from_orm(personal)
    )


# ============================================================================
# DATA MANAGEMENT (Admin Only)
# ============================================================================

@router.patch("", response_model=StandardResponse)
async def update_personal_info(
    updates: PersonalUpdate,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin_user)
):
    """
    Update personal information (Admin only).
    
    Updates only the provided fields. Creates the record if it doesn't exist.
    
    Args:
        updates: Fields to update
        db: Database session
        current_admin: Authenticated admin user (dependency)
        
    Returns:
        StandardResponse with updated Personal record
    """
    personal = db.query(Personal).filter(Personal.is_deleted == False).first()
    
    if not personal:
        # Create new if doesn't exist (Singleton pattern)
        personal = Personal()
        db.add(personal)
    
    # Update only provided fields (exclude_unset=True)
    update_data = updates.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(personal, field, value)
    
    db.commit()
    db.refresh(personal)
    
    return StandardResponse(
        success=True,
        message="Personal information updated successfully",
        data=PersonalResponse.from_orm(personal)
    )


# ============================================================================
# FILE UPLOADS (Admin Only)
# ============================================================================

@router.post("/upload-profile-pic", response_model=StandardResponse)
async def upload_profile_pic(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin_user)
):
    """
    Upload profile picture (Admin only).
    
    Validates that the file is an image, saves it to storage,
    and updates the database record.
    """
    # Save file using service (handles validation and storage)
    file_path = await save_upload_file(file, db, is_image=True)
    
    # Get or create personal record
    personal = db.query(Personal).filter(Personal.is_deleted == False).first()
    if not personal:
        personal = Personal()
        db.add(personal)
    
    # Update record
    personal.profile_pic = file_path
    db.commit()
    
    return StandardResponse(
        success=True,
        message="Profile picture uploaded successfully",
        data={"file_path": file_path}
    )


@router.post("/upload-cv", response_model=StandardResponse)
async def upload_cv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin_user)
):
    """
    Upload CV/Resume PDF (Admin only).
    
    Validates that the file is a PDF/document, saves it to storage,
    and updates the database record.
    """
    # Save file using service (is_image=False allows PDFs)
    file_path = await save_upload_file(file, db, is_image=False)
    
    # Get or create personal record
    personal = db.query(Personal).filter(Personal.is_deleted == False).first()
    if not personal:
        personal = Personal()
        db.add(personal)
    
    # Update record
    personal.cv_file = file_path
    db.commit()
    
    return StandardResponse(
        success=True,
        message="CV uploaded successfully",
        data={"file_path": file_path}
    )
