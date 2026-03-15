"""
Articles API Endpoints
=====================

This module defines endpoints for managing blog articles.
Articles support rich text content and featured status.

Features:
    - List all articles (Public)
    - Filter featured articles (Public)
    - Get article by slug (Public)
    - Create new article (Admin)
    - Update existing article (Admin)
    - Soft delete article (Admin)
    - Upload cover image (Admin)
    - Upload PDF attachment (Admin)

Routes:
    - GET /: List articles
    - GET /{slug}: Get article details
    - POST /: Create article
    - PATCH /{id}: Update article
    - DELETE /{id}: Delete article
    - POST /{id}/upload-cover: Upload cover image
    - POST /{id}/upload-pdf: Upload PDF attachment
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from ...database import get_db
from ...models.article import Article
from ...schemas.common import StandardResponse
from ...core.deps import get_current_admin_user
from ...services.file_service import save_upload_file
from ...services.slug_service import generate_unique_slug
from ...services.sanitize_service import sanitize_html

router = APIRouter()


# ============================================================================
# SCHEMAS
# ============================================================================

class ArticleCreate(BaseModel):
    """Schema for creating a new article."""
    title: str
    slug: Optional[str] = None
    excerpt: str
    body: Optional[str] = None
    external_url: Optional[str] = None
    is_featured: bool = False


class ArticleUpdate(BaseModel):
    """Schema for updating an article (partial updates)."""
    title: Optional[str] = None
    slug: Optional[str] = None
    excerpt: Optional[str] = None
    body: Optional[str] = None
    external_url: Optional[str] = None
    is_featured: Optional[bool] = None


class ArticleResponse(BaseModel):
    """Schema for article response."""
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
async def list_articles(
    featured: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """
    List all active articles (Public).
    Optionally filter by featured status.
    """
    query = db.query(Article).filter(Article.is_deleted == False)
    
    if featured is not None:
        query = query.filter(Article.is_featured == featured)
        
    articles = query.order_by(Article.created_at.desc()).all()
    
    return StandardResponse(
        success=True,
        message=f"Retrieved {len(articles)} articles",
        data=[ArticleResponse.from_orm(a) for a in articles]
    )


@router.get("/{slug}", response_model=StandardResponse)
async def get_article(slug: str, db: Session = Depends(get_db)):
    """
    Get article details by slug (Public).
    """
    article = db.query(Article).filter(
        Article.slug == slug,
        Article.is_deleted == False
    ).first()
    
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
    
    return StandardResponse(
        success=True,
        message="Article retrieved successfully",
        data=ArticleResponse.from_orm(article)
    )


# ============================================================================
# CREATE OPERATIONS (Admin Only)
# ============================================================================

@router.post("", response_model=StandardResponse)
async def create_article(
    article_data: ArticleCreate,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin_user)
):
    """
    Create a new article (Admin only).
    """
    provided_slug = (article_data.slug or "").strip()
    slug = provided_slug or generate_unique_slug(article_data.title, Article, db)

    # Check for duplicate slug
    existing = db.query(Article).filter(
        Article.slug == slug,
        Article.is_deleted == False
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Article with this slug already exists"
        )

    article_payload = article_data.dict()
    article_payload["slug"] = slug
    if article_payload.get("body"):
        article_payload["body"] = sanitize_html(article_payload["body"])

    article = Article(**article_payload)
    db.add(article)
    db.commit()
    db.refresh(article)
    
    return StandardResponse(
        success=True,
        message="Article created successfully",
        data=ArticleResponse.from_orm(article)
    )


# ============================================================================
# UPDATE OPERATIONS (Admin Only)
# ============================================================================

@router.patch("/{article_id}", response_model=StandardResponse)
async def update_article(
    article_id: str,
    updates: ArticleUpdate,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin_user)
):
    """
    Update an article (Admin only).
    """
    article = db.query(Article).filter(
        Article.id == article_id,
        Article.is_deleted == False
    ).first()
    
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
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
    if "slug" in update_data and update_data["slug"] != article.slug:
        existing = db.query(Article).filter(
            Article.slug == update_data["slug"],
            Article.is_deleted == False
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Article with this slug already exists"
            )

    if "body" in update_data and update_data["body"] is not None:
        update_data["body"] = sanitize_html(update_data["body"])

    for field, value in update_data.items():
        setattr(article, field, value)
    
    db.commit()
    db.refresh(article)
    
    return StandardResponse(
        success=True,
        message="Article updated successfully",
        data=ArticleResponse.from_orm(article)
    )


# ============================================================================
# DELETE OPERATIONS (Admin Only)
# ============================================================================

@router.delete("/{article_id}", response_model=StandardResponse)
async def delete_article(
    article_id: str,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin_user)
):
    """
    Soft delete an article (Admin only).
    """
    article = db.query(Article).filter(
        Article.id == article_id,
        Article.is_deleted == False
    ).first()
    
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
    
    article.is_deleted = True
    db.commit()
    
    return StandardResponse(
        success=True,
        message="Article deleted successfully",
        data=None
    )


# ============================================================================
# FILE UPLOADS (Admin Only)
# ============================================================================

@router.post("/{article_id}/upload-cover", response_model=StandardResponse)
async def upload_article_cover(
    article_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin_user)
):
    """
    Upload article cover image (Admin only).
    """
    article = db.query(Article).filter(
        Article.id == article_id,
        Article.is_deleted == False
    ).first()
    
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
    
    file_path = await save_upload_file(file, db, is_image=True)
    article.cover_image = file_path
    db.commit()
    
    return StandardResponse(
        success=True,
        message="Cover image uploaded successfully",
        data={"file_path": file_path}
    )


@router.post("/{article_id}/upload-pdf", response_model=StandardResponse)
async def upload_article_pdf(
    article_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin_user)
):
    """
    Upload article PDF attachment (Admin only).
    """
    article = db.query(Article).filter(
        Article.id == article_id,
        Article.is_deleted == False
    ).first()
    
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
    
    file_path = await save_upload_file(file, db, is_image=False)
    article.pdf_attachment = file_path
    db.commit()
    
    return StandardResponse(
        success=True,
        message="PDF uploaded successfully",
        data={"file_path": file_path}
    )
