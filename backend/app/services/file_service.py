import uuid
from io import BytesIO
from fastapi import UploadFile, HTTPException, status
from PIL import Image
import filetype
import cloudinary
import cloudinary.uploader
from sqlalchemy.orm import Session
from ..config import get_settings

settings = get_settings()

# Configure Cloudinary
cloudinary.config(
    cloud_name=settings.cloudinary_cloud_name,
    api_key=settings.cloudinary_api_key,
    api_secret=settings.cloudinary_api_secret,
    secure=True
)

ALLOWED_IMAGE_TYPES = ['image/png', 'image/jpeg', 'image/webp']
ALLOWED_PDF_TYPE = 'application/pdf'


def validate_file_type(file_content: bytes, expected_types: list) -> str:
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
    content = await upload_file.read()

    if is_image:
        file_type = validate_file_type(content, ALLOWED_IMAGE_TYPES)
        max_size = settings.max_image_size_bytes
    else:
        file_type = validate_file_type(content, [ALLOWED_PDF_TYPE])
        max_size = settings.max_pdf_size_bytes

    validate_file_size(len(content), max_size)

    unique_id = str(uuid.uuid4())

    try:
        if is_image:
            # Convert to WebP first
            img = Image.open(BytesIO(content))
            img = img.convert('RGB')
            buffer = BytesIO()
            img.save(buffer, "WEBP", quality=85, optimize=True)
            buffer.seek(0)

            result = cloudinary.uploader.upload(
                buffer,
                public_id=f"portfolio/images/{unique_id}",
                resource_type="image",
                format="webp"
            )
        else:
            # Upload PDF directly
            result = cloudinary.uploader.upload(
                BytesIO(content),
                public_id=f"portfolio/pdfs/{unique_id}",
                resource_type="raw",
                format="pdf",
                flags="attachment",
                use_filename=True
                unique_filename=False
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error uploading file: {str(e)}"
        )

    # Return the Cloudinary URL
    return result["secure_url"]


def delete_file(file_path: str, db: Session = None) -> None:
    if not file_path:
        return
    try:
        # Extract public_id from Cloudinary URL
        if "cloudinary.com" in file_path:
            # e.g. .../portfolio/images/uuid.webp
            parts = file_path.split("/upload/")
            if len(parts) == 2:
                public_id = parts[1].rsplit(".", 1)[0]  # remove extension
                cloudinary.uploader.destroy(public_id)
    except Exception:
        pass  # Don't crash if delete fails
