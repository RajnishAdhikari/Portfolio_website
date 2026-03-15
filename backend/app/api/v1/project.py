"""
Projects API Endpoints
=====================

This module defines endpoints for managing portfolio projects.
Projects are the core content, showcasing work with rich details and media.

Features:
    - List all projects (Public)
    - Get project by slug (Public)
    - Create new project (Admin)
    - Update existing project (Admin)
    - Soft delete project (Admin)
    - Upload cover image (Admin)
    - Upload gallery images (Admin)
    - Upload PDF attachment (Admin)

Routes:
    - GET /: List projects
    - GET /{slug}: Get project details
    - POST /: Create project
    - PATCH /{id}: Update project
    - DELETE /{id}: Delete project
    - POST /{id}/upload-cover: Upload cover image
    - POST /{id}/upload-image: Add image to gallery
    - POST /{id}/upload-pdf: Upload PDF attachment
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional, Any
from pydantic import BaseModel
from datetime import datetime

from ...database import get_db
from ...models.project import Project
from ...schemas.common import StandardResponse
from ...core.deps import get_current_admin_user
from ...services.file_service import save_upload_file
from ...services.slug_service import generate_unique_slug
from ...services.sanitize_service import sanitize_html

router = APIRouter()


# ============================================================================
# SCHEMAS
# ============================================================================

class ProjectCreate(BaseModel):
    """Schema for creating a new project."""
    title: str
    slug: Optional[str] = None
    short_desc: str
    detailed_desc: Optional[str] = None
    tech_stack: Optional[List[str]] = None
    external_url: Optional[str] = None
    github_url: Optional[str] = None
    images: Optional[List[str]] = None


class ProjectUpdate(BaseModel):
    """Schema for updating a project (partial updates)."""
    title: Optional[str] = None
    slug: Optional[str] = None
    short_desc: Optional[str] = None
    detailed_desc: Optional[str] = None
    tech_stack: Optional[List[str]] = None
    external_url: Optional[str] = None
    github_url: Optional[str] = None
    images: Optional[List[str]] = None  # To reorder or remove images


class ProjectResponse(BaseModel):
    """Schema for project response."""
    id: str
    title: str
    slug: str
    short_desc: str
    detailed_desc: Optional[str]
    cover_image: Optional[str]
    images: Optional[List[str]]
    pdf_attachment: Optional[str]
    external_url: Optional[str]
    github_url: Optional[str]
    tech_stack: Optional[List[str]]
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================================
# READ OPERATIONS (Public)
# ============================================================================

@router.get("", response_model=StandardResponse)
async def list_projects(db: Session = Depends(get_db)):
    """
    List all active projects (Public).
    
    Returns a list of projects ordered by creation date (descending).
    """
    projects = db.query(Project).filter(
        Project.is_deleted == False
    ).order_by(Project.created_at.desc()).all()
    
    return StandardResponse(
        success=True,
        message=f"Retrieved {len(projects)} projects",
        data=[ProjectResponse.from_orm(p) for p in projects]
    )


@router.get("/{slug}", response_model=StandardResponse)
async def get_project(slug: str, db: Session = Depends(get_db)):
    """
    Get project details by slug (Public).
    """
    project = db.query(Project).filter(
        Project.slug == slug,
        Project.is_deleted == False
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    return StandardResponse(
        success=True,
        message="Project retrieved successfully",
        data=ProjectResponse.from_orm(project)
    )


# ============================================================================
# CREATE OPERATIONS (Admin Only)
# ============================================================================

@router.post("", response_model=StandardResponse)
async def create_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin_user)
):
    """
    Create a new project (Admin only).
    """
    provided_slug = (project_data.slug or "").strip()
    slug = provided_slug or generate_unique_slug(project_data.title, Project, db)
    existing = db.query(Project).filter(Project.slug == slug, Project.is_deleted == False).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Project with this slug already exists"
        )

    project_payload = project_data.dict()
    project_payload["slug"] = slug
    if project_payload.get("detailed_desc"):
        project_payload["detailed_desc"] = sanitize_html(project_payload["detailed_desc"])

    project = Project(**project_payload)
    db.add(project)
    db.commit()
    db.refresh(project)
    
    return StandardResponse(
        success=True,
        message="Project created successfully",
        data=ProjectResponse.from_orm(project)
    )


# ============================================================================
# UPDATE OPERATIONS (Admin Only)
# ============================================================================

@router.patch("/{project_id}", response_model=StandardResponse)
async def update_project(
    project_id: str,
    updates: ProjectUpdate,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin_user)
):
    """
    Update a project (Admin only).
    """
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.is_deleted == False
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
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
    if "slug" in update_data and update_data["slug"] != project.slug:
        existing = db.query(Project).filter(
            Project.slug == update_data["slug"],
            Project.is_deleted == False
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Project with this slug already exists"
            )

    if "detailed_desc" in update_data and update_data["detailed_desc"] is not None:
        update_data["detailed_desc"] = sanitize_html(update_data["detailed_desc"])

    for field, value in update_data.items():
        setattr(project, field, value)
    
    db.commit()
    db.refresh(project)
    
    return StandardResponse(
        success=True,
        message="Project updated successfully",
        data=ProjectResponse.from_orm(project)
    )


# ============================================================================
# DELETE OPERATIONS (Admin Only)
# ============================================================================

@router.delete("/{project_id}", response_model=StandardResponse)
async def delete_project(
    project_id: str,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin_user)
):
    """
    Soft delete a project (Admin only).
    """
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.is_deleted == False
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    project.is_deleted = True
    db.commit()
    
    return StandardResponse(
        success=True,
        message="Project deleted successfully",
        data=None
    )


# ============================================================================
# FILE UPLOADS (Admin Only)
# ============================================================================

@router.post("/{project_id}/upload-cover", response_model=StandardResponse)
async def upload_project_cover(
    project_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin_user)
):
    """
    Upload project cover image (Admin only).
    """
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.is_deleted == False
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    file_path = await save_upload_file(file, db, is_image=True)
    project.cover_image = file_path
    db.commit()
    
    return StandardResponse(
        success=True,
        message="Cover image uploaded successfully",
        data={"file_path": file_path}
    )


@router.post("/{project_id}/upload-image", response_model=StandardResponse)
async def upload_project_image(
    project_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin_user)
):
    """
    Add an image to the project gallery (Admin only).
    Appends the new image path to the images list.
    """
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.is_deleted == False
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    file_path = await save_upload_file(file, db, is_image=True)
    
    # Initialize list if None
    current_images = project.images or []
    # Create new list to ensure change tracking detection
    new_images = list(current_images)
    new_images.append(file_path)
    
    project.images = new_images
    db.commit()
    
    return StandardResponse(
        success=True,
        message="Gallery image uploaded successfully",
        data={"file_path": file_path}
    )


@router.post("/{project_id}/upload-pdf", response_model=StandardResponse)
async def upload_project_pdf(
    project_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin_user)
):
    """
    Upload project PDF attachment (Admin only).
    """
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.is_deleted == False
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    file_path = await save_upload_file(file, db, is_image=False)
    project.pdf_attachment = file_path
    db.commit()
    
    return StandardResponse(
        success=True,
        message="PDF uploaded successfully",
        data={"file_path": file_path}
    )
