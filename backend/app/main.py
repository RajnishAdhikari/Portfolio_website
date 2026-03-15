"""FastAPI application entrypoint."""

import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .api.v1.router import api_router
from .config import get_settings
from .core.middleware import setup_cors, setup_rate_limiting
from .database import Base, engine
from .schemas.common import StandardResponse

settings = get_settings()
is_dev = settings.environment.lower() == "dev"

app = FastAPI(
    title="Portfolio API",
    description="Backend API for dynamic portfolio website",
    version="1.0.0",
    debug=is_dev,
)

# Middleware
setup_cors(app)
setup_rate_limiting(app)

# API routes
app.include_router(api_router, prefix="/api/v1")

# Static uploads
upload_dir = settings.upload_dir
os.makedirs(upload_dir, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=upload_dir), name="uploads")

# Auto-create tables in dev only
if is_dev:
    Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    return {
        "message": "Portfolio API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health", response_model=StandardResponse)
async def health():
    return StandardResponse(
        success=True,
        message="API is healthy",
        data={"status": "ok"},
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=is_dev,
    )
