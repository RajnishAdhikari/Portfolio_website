import os
import uuid
from io import BytesIO
from fastapi import UploadFile, HTTPException, status
from PIL import Image
import filetype
from sqlalchemy.orm import Session
from ..config import get_settings

settings = get_settings()

# Allowed file types
ALLOWED_IMAGE_TYPES = ['image/png', 'image/jpeg', 'image/webp']
ALLOWED_PDF_TYPE = 'application/pdf'


def validate_file_type(file_content: bytes, expected_types: list) -> str:
    """
    Validate file type using magic bytes
    
    Args:
        file_content: File content bytes
        expected_types: List of allowed MIME types
    
    Returns:
        Detected MIME type
    
    Raises:
        HTTPException: If file type is not allowed
    """
    kind = filetype.guess(file_content)
    
    if kind is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to determine file type"
        )
    
    if kind.mime not in expected_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type {kind.mime} is not allowed. Allowed types: {expected_types}"
        )
    
    return kind.mime


def validate_file_size(file_size: int, max_size: int) -> None:
    """
    Validate file size
    
    Args:
        file_size: Size in bytes
        max_size: Maximum allowed size in bytes
    
    Raises:
        HTTPException: If file is too large
    """
    if file_size > max_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File too large. Maximum size: {max_size / (1024 * 1024):.1f}MB"
        )


async def save_upload_file(
    upload_file: UploadFile,
    db: Session,
    is_image: bool = True
) -> str:
    """
    Save uploaded file to disk
    
    Args:
        upload_file: FastAPI UploadFile object
        db: Database session (not used, kept for compatibility)
        is_image: Whether file is an image (True) or PDF (False)
    
    Returns:
        File path string
    """
    # Read file content
    content = await upload_file.read()
    
    # Validate file type
    if is_image:
        file_type = validate_file_type(content, ALLOWED_IMAGE_TYPES)
        max_size = settings.max_image_size_bytes
    else:
        file_type = validate_file_type(content, [ALLOWED_PDF_TYPE])
        max_size = settings.max_pdf_size_bytes
    
    # Validate file size
    validate_file_size(len(content), max_size)
    
    # Create upload directory if it doesn't exist
    os.makedirs(settings.upload_dir, exist_ok=True)

    # Build deterministic file names and return web-accessible URL paths.
    unique_stem = str(uuid.uuid4())

    if is_image:
        try:
            img = Image.open(BytesIO(content))

            # Convert to WebP and compress if needed
            if file_type != 'image/webp' or len(content) > 200 * 1024:
                img = img.convert('RGB')
                filename = f"{unique_stem}.webp"
                disk_path = os.path.join(settings.upload_dir, filename)
                img.save(disk_path, "WEBP", quality=85, optimize=True)
            else:
                ext = ".webp" if file_type == "image/webp" else (".png" if file_type == "image/png" else ".jpg")
                filename = f"{unique_stem}{ext}"
                disk_path = os.path.join(settings.upload_dir, filename)
                with open(disk_path, 'wb') as f:
                    f.write(content)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error processing image: {str(e)}"
            )
    else:
        # Save PDF as is
        filename = f"{unique_stem}.pdf"
        disk_path = os.path.join(settings.upload_dir, filename)
        with open(disk_path, 'wb') as f:
            f.write(content)

    # Store path as URL path, never as OS path.
    return f"/uploads/{filename}"


def delete_file(file_path: str, db: Session = None) -> None:
    """
    Delete file from disk
    
    Args:
        file_path: Path to file
        db: Database session (not used, kept for compatibility)
    """
    if not file_path:
        return

    normalized = file_path.replace("\\", "/")

    if normalized.startswith("/uploads/"):
        disk_path = os.path.join(settings.upload_dir, os.path.basename(normalized))
    elif normalized.startswith("uploads/"):
        disk_path = os.path.join(settings.upload_dir, os.path.basename(normalized))
    elif os.path.isabs(file_path):
        disk_path = file_path
    else:
        disk_path = file_path

    if os.path.exists(disk_path):
        os.remove(disk_path)
