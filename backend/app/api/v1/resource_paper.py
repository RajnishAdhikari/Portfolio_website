"""
Resource Paper API Endpoints
===========================

This module defines endpoints for managing research papers and resources.
Supports PDF attachments and research-focused metadata.

Features:
    - List all papers (Public)
    - Filter featured papers (Public)
    - Get paper by slug (Public)
    - Create new paper (Admin)
    - Update existing paper (Admin)
    - Soft delete paper (Admin)
    - Upload cover image (Admin)
    - Upload PDF attachment (Admin)

Routes:
    - GET /: List papers
    - GET /{slug}: Get paper details
    - POST /: Create paper
    - PATCH /{id}: Update paper
    - DELETE /{id}: Delete paper
    - POST /{id}/upload-cover: Upload cover image
    - POST /{id}/upload-pdf: Upload PDF
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from ...database import get_db
from ...models.resource_paper import ResourcePaper
from ...schemas.common import StandardResponse
from ...core.deps import get_current_admin_user
from ...services.file_service import save_upload_file
from ...services.slug_service import generate_unique_slug
from ...services.sanitize_service import sanitize_html

router = APIRouter()


# ============================================================================
# SCHEMAS
# ============================================================================

class ResourcePaperCreate(BaseModel):
    """Schema for creating a new resource paper."""
    title: str
    slug: Optional[str] = None
    excerpt: str
    body: Optional[str] = None
    external_url: Optional[str] = None
    is_featured: bool = False


class ResourcePaperUpdate(BaseModel):
    """Schema for updating a resource paper (partial updates)."""
    title: Optional[str] = None
    slug: Optional[str] = None
    excerpt: Optional[str] = None
    body: Optional[str] = None
    external_url: Optional[str] = None
    is_featured: Optional[bool] = None


class ResourcePaperResponse(BaseModel):
    """Schema for resource paper response."""
    id: str
    title: str
    slug: str
    excerpt: str
    body: Optional[str]
    cover_image: Optional[str]
    pdf_attachment: Optional[str]
    external_url: Optional[str]
    is_featured: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================================
# READ OPERATIONS (Public)
# ============================================================================

@router.get("", response_model=StandardResponse)
async def list_papers(
    featured: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """
    List all active resource papers (Public).
    Optionally filter by featured status.
    """
    query = db.query(ResourcePaper).filter(ResourcePaper.is_deleted == False)
    
    if featured is not None:
        query = query.filter(ResourcePaper.is_featured == featured)
        
    papers = query.order_by(ResourcePaper.created_at.desc()).all()
    
    return StandardResponse(
        success=True,
        message=f"Retrieved {len(papers)} resource papers",
        data=[ResourcePaperResponse.from_orm(p) for p in papers]
    )


@router.get("/{slug}", response_model=StandardResponse)
async def get_paper(slug: str, db: Session = Depends(get_db)):
    """
    Get paper details by slug (Public).
    """
    paper = db.query(ResourcePaper).filter(
        ResourcePaper.slug == slug,
        ResourcePaper.is_deleted == False
    ).first()
    
    if not paper:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource paper not found"
        )
    
    return StandardResponse(
        success=True,
        message="Resource paper retrieved successfully",
        data=ResourcePaperResponse.from_orm(paper)
    )


# ============================================================================
# CREATE OPERATIONS (Admin Only)
# ============================================================================

@router.post("", response_model=StandardResponse)
async def create_paper(
    paper_data: ResourcePaperCreate,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin_user)
):
    """
    Create a new resource paper (Admin only).
    """
    provided_slug = (paper_data.slug or "").strip()
    slug = provided_slug or generate_unique_slug(paper_data.title, ResourcePaper, db)

    # Check for duplicate slug
    existing = db.query(ResourcePaper).filter(
        ResourcePaper.slug == slug,
        ResourcePaper.is_deleted == False
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Paper with this slug already exists"
        )

    paper_payload = paper_data.dict()
    paper_payload["slug"] = slug
    if paper_payload.get("body"):
        paper_payload["body"] = sanitize_html(paper_payload["body"])

    paper = ResourcePaper(**paper_payload)
    db.add(paper)
    db.commit()
    db.refresh(paper)
    
    return StandardResponse(
        success=True,
        message="Resource paper created successfully",
        data=ResourcePaperResponse.from_orm(paper)
    )


# ============================================================================
# UPDATE OPERATIONS (Admin Only)
# ============================================================================

@router.patch("/{paper_id}", response_model=StandardResponse)
async def update_paper(
    paper_id: str,
    updates: ResourcePaperUpdate,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin_user)
):
    """
    Update a resource paper (Admin only).
    """
    paper = db.query(ResourcePaper).filter(
        ResourcePaper.id == paper_id,
        ResourcePaper.is_deleted == False
    ).first()
    
    if not paper:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource paper not found"
        )
    
    update_data = updates.dict(exclude_unset=True)
    
    # Check slug uniqueness if changing
    if "slug" in update_data:
        slug_candidate = (update_data["slug"] or "").strip()
        if not slug_candidate:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Slug cannot be empty"
            )
        update_data["slug"] = slug_candidate
    if "slug" in update_data and update_data["slug"] != paper.slug:
        existing = db.query(ResourcePaper).filter(
            ResourcePaper.slug == update_data["slug"],
            ResourcePaper.is_deleted == False
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Paper with this slug already exists"
            )

    if "body" in update_data and update_data["body"] is not None:
        update_data["body"] = sanitize_html(update_data["body"])

    for field, value in update_data.items():
        setattr(paper, field, value)
    
    db.commit()
    db.refresh(paper)
    
    return StandardResponse(
        success=True,
        message="Resource paper updated successfully",
        data=ResourcePaperResponse.from_orm(paper)
    )


# ============================================================================
# DELETE OPERATIONS (Admin Only)
# ============================================================================

@router.delete("/{paper_id}", response_model=StandardResponse)
async def delete_paper(
    paper_id: str,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin_user)
):
    """
    Soft delete a resource paper (Admin only).
    """
    paper = db.query(ResourcePaper).filter(
        ResourcePaper.id == paper_id,
        ResourcePaper.is_deleted == False
    ).first()
    
    if not paper:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource paper not found"
        )
    
    paper.is_deleted = True
    db.commit()
    
    return StandardResponse(
        success=True,
        message="Resource paper deleted successfully",
        data=None
    )


# ============================================================================
# FILE UPLOADS (Admin Only)
# ============================================================================

@router.post("/{paper_id}/upload-cover", response_model=StandardResponse)
async def upload_paper_cover(
    paper_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin_user)
):
    """
    Upload paper cover image (Admin only).
    """
    paper = db.query(ResourcePaper).filter(
        ResourcePaper.id == paper_id,
        ResourcePaper.is_deleted == False
    ).first()
    
    if not paper:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource paper not found"
        )
    
    file_path = await save_upload_file(file, db, is_image=True)
    paper.cover_image = file_path
    db.commit()
    
    return StandardResponse(
        success=True,
        message="Cover image uploaded successfully",
        data={"file_path": file_path}
    )


@router.post("/{paper_id}/upload-pdf", response_model=StandardResponse)
async def upload_paper_pdf(
    paper_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin_user)
):
    """
    Upload paper PDF attachment (Admin only).
    """
    paper = db.query(ResourcePaper).filter(
        ResourcePaper.id == paper_id,
        ResourcePaper.is_deleted == False
    ).first()
    
    if not paper:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource paper not found"
        )
    
    file_path = await save_upload_file(file, db, is_image=False)
    paper.pdf_attachment = file_path
    db.commit()
    
    return StandardResponse(
        success=True,
        message="PDF uploaded successfully",
        data={"file_path": file_path}
    )
