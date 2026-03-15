from fastapi import APIRouter
from ...schemas.common import StandardResponse

router = APIRouter()


@router.get("/health", response_model=StandardResponse)
async def health_check():
    """Health check endpoint for monitoring"""
    return StandardResponse(
        success=True,
        message="API is healthy",
        data={"status": "ok"}
    )
