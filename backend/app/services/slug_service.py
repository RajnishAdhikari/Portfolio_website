from slugify import slugify
from sqlalchemy.orm import Session
from typing import Type
from ..database import Base


def generate_unique_slug(title: str, model: Type[Base], db: Session) -> str:
    """
    Generate a unique slug from title
    
    Args:
        title: Title to slugify
        model: SQLAlchemy model class with slug field
        db: Database session
    
    Returns:
        Unique slug string
    """
    base_slug = slugify(title)
    slug = base_slug
    counter = 1
    
    # Keep incrementing counter until we find a unique slug
    while db.query(model).filter(
        model.slug == slug,
        model.is_deleted == False
    ).first() is not None:
        slug = f"{base_slug}-{counter}"
        counter += 1
    
    return slug
