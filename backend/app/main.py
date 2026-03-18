"""FastAPI application entrypoint."""

import os
import logging
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .api.v1.router import api_router
from .config import get_settings
from .core.security import get_password_hash
from .core.middleware import setup_cors, setup_rate_limiting
from .database import Base, SessionLocal, engine
from .models.user import User, UserRole
from .schemas.common import StandardResponse

settings = get_settings()
is_dev = settings.environment.lower() == "dev"
logger = logging.getLogger(__name__)

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

# Auto-create tables in dev or when explicitly enabled for first-time deploys
if is_dev or settings.auto_create_tables:
    Base.metadata.create_all(bind=engine)


def bootstrap_admin_user() -> None:
    """
    Create (or optionally reset) an admin user from environment variables.
    Useful for free-tier hosts where shell/one-off jobs are unavailable.
    """
    email = settings.bootstrap_admin_email.strip().lower()
    password = settings.bootstrap_admin_password

    if not email or not password:
        return

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            db.add(
                User(
                    email=email,
                    hashed_password=get_password_hash(password),
                    role=UserRole.ADMIN,
                )
            )
            db.commit()
            logger.info("Bootstrapped admin user: %s", email)
            return

        if settings.bootstrap_admin_force_reset:
            user.hashed_password = get_password_hash(password)
            user.role = UserRole.ADMIN
            user.is_deleted = False
            db.commit()
            logger.info("Reset bootstrap admin credentials for: %s", email)
    finally:
        db.close()


@app.on_event("startup")
async def startup_tasks():
    bootstrap_admin_user()


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
