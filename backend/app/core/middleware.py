from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from ..config import get_settings

settings = get_settings()

# Rate limiter instance
limiter = Limiter(key_func=get_remote_address)


def setup_cors(app):
    """Configure CORS middleware"""
    # Parse CORS origins
    origins = settings.cors_origins_list

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )


def setup_rate_limiting(app):
    """Configure rate limiting"""
    app.state.limiter = limiter
    app.add_middleware(SlowAPIMiddleware)
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
