from typing import Any, Optional
from pydantic import BaseModel


class StandardResponse(BaseModel):
    """Standardized API response format"""
    success: bool
    message: str
    data: Optional[Any] = None
