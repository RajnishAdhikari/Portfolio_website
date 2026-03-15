"""
Certification API Endpoints
==========================

This module defines endpoints for managing professional certifications.
Certifications serve as proof of expertise and continuous learning.

Features:
    - List all certifications (Public)
    - Create new certification (Admin)
    - Update existing certification (Admin)
    - Soft delete certification (Admin)
    - Upload certificate image (Admin)

Routes:
    - GET /: List certifications
    - POST /: Create certification
    - PATCH /{id}: Update certification
    - DELETE /{id}: Delete certification
    - POST /{id}/upload-image: Upload certificate image
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from ...database import get_db
from ...models.certification import Certification
from ...schemas.common import StandardResponse
from ...core.deps import get_current_admin_user
from ...services.file_service import save_upload_file
from ...services.sanitize_service import sanitize_html

router = APIRouter()


# ============================================================================
# SCHEMAS
# ============================================================================

class CertificationCreate(BaseModel):
    """Schema for creating a new certification."""
    name: str
    issuer: str
    issue_month_year: str
    cred_id: Optional[str] = None
    cred_url: Optional[str] = None
    description: Optional[str] = None


class CertificationUpdate(BaseModel):
    """Schema for updating a certification (partial updates)."""
    name: Optional[str] = None
    issuer: Optional[str] = None
    issue_month_year: Optional[str] = None
    cred_id: Optional[str] = None
    cred_url: Optional[str] = None
    description: Optional[str] = None


class CertificationResponse(BaseModel):
    """Schema for certification response."""
    id: str
    name: str
    issuer: str
    issue_month_year: str
    cred_id: Optional[str]
    cred_url: Optional[str]
    description: Optional[str]
    image: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================================
# READ OPERATIONS (Public)
# ============================================================================

@router.get("", response_model=StandardResponse)
async def list_certifications(db: Session = Depends(get_db)):
    """
    List all active certifications (Public).
    
    Returns a list of certifications ordered by issue date (descending).
    """
    certs = db.query(Certification).filter(
        Certification.is_deleted == False
    ).order_by(Certification.issue_month_year.desc()).all()
    
    return StandardResponse(
        success=True,
        message=f"Retrieved {len(certs)} certifications",
        data=[CertificationResponse.from_orm(c) for c in certs]
    )


# ============================================================================
# CREATE OPERATIONS (Admin Only)
# ============================================================================

@router.post("", response_model=StandardResponse)
async def create_certification(
    cert_data: CertificationCreate,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin_user)
):
    """
    Create a new certification (Admin only).
    """
    payload = cert_data.dict()
    if payload.get("description"):
        payload["description"] = sanitize_html(payload["description"])

    cert = Certification(**payload)
    db.add(cert)
    db.commit()
    db.refresh(cert)
    
    return StandardResponse(
        success=True,
        message="Certification created successfully",
        data=CertificationResponse.from_orm(cert)
    )


# ============================================================================
# UPDATE OPERATIONS (Admin Only)
# ============================================================================

@router.patch("/{cert_id}", response_model=StandardResponse)
async def update_certification(
    cert_id: str,
    updates: CertificationUpdate,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin_user)
):
    """
    Update a certification (Admin only).
    """
    cert = db.query(Certification).filter(
        Certification.id == cert_id,
        Certification.is_deleted == False
    ).first()
    
    if not cert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certification not found"
        )
    
    update_data = updates.dict(exclude_unset=True)
    if "description" in update_data and update_data["description"] is not None:
        update_data["description"] = sanitize_html(update_data["description"])
    for field, value in update_data.items():
        setattr(cert, field, value)
    
    db.commit()
    db.refresh(cert)
    
    return StandardResponse(
        success=True,
        message="Certification updated successfully",
        data=CertificationResponse.from_orm(cert)
    )


# ============================================================================
# DELETE OPERATIONS (Admin Only)
# ============================================================================

@router.delete("/{cert_id}", response_model=StandardResponse)
async def delete_certification(
    cert_id: str,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin_user)
):
    """
    Soft delete a certification (Admin only).
    """
    cert = db.query(Certification).filter(
        Certification.id == cert_id,
        Certification.is_deleted == False
    ).first()
    
    if not cert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certification not found"
        )
    
    cert.is_deleted = True
    db.commit()
    
    return StandardResponse(
        success=True,
        message="Certification deleted successfully",
        data=None
    )


# ============================================================================
# FILE UPLOADS (Admin Only)
# ============================================================================

@router.post("/{cert_id}/upload-image", response_model=StandardResponse)
async def upload_certification_image(
    cert_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin_user)
):
    """
    Upload certificate image/scan (Admin only).
    """
    cert = db.query(Certification).filter(
        Certification.id == cert_id,
        Certification.is_deleted == False
    ).first()
    
    if not cert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certification not found"
        )
    
    file_path = await save_upload_file(file, db, is_image=True)
    cert.image = file_path
    db.commit()
    
    return StandardResponse(
        success=True,
        message="Certificate image uploaded successfully",
        data={"file_path": file_path}
    )
