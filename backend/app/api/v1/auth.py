"""Authentication API endpoints."""

from datetime import datetime, timedelta
from typing import Optional, Tuple

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from ...config import get_settings
from ...core.deps import get_current_admin_user, get_current_user
from ...core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    get_password_hash,
    verify_password,
    verify_token_type,
)
from ...database import get_db
from ...models.refresh_token import RefreshToken
from ...models.user import User, UserRole
from ...schemas.auth import LoginRequest
from ...schemas.common import StandardResponse

router = APIRouter()
settings = get_settings()

REFRESH_COOKIE_NAME = "refresh_token"


class RefreshRequest(BaseModel):
    refresh_token: Optional[str] = None


class LogoutRequest(BaseModel):
    refresh_token: Optional[str] = None


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    role: str = UserRole.CONTRIBUTOR.value


def _is_production() -> bool:
    return settings.environment.lower() in {"prod", "production"}


def _set_refresh_cookie(response: Response, refresh_token: str) -> None:
    is_production = _is_production()
    response.set_cookie(
        key=REFRESH_COOKIE_NAME,
        value=refresh_token,
        httponly=True,
        secure=is_production,
        samesite="none" if is_production else "lax",
        max_age=settings.refresh_token_expire_days * 24 * 60 * 60,
        path="/",
    )


def _clear_refresh_cookie(response: Response) -> None:
    response.delete_cookie(key=REFRESH_COOKIE_NAME, path="/")


def _issue_tokens_for_user(user: User, db: Session) -> Tuple[str, str]:
    access_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.id, "role": user.role.value},
        expires_delta=access_expires,
    )
    refresh_token = create_refresh_token(
        data={"sub": user.id, "role": user.role.value},
    )

    db.add(
        RefreshToken(
            user_id=user.id,
            refresh_token_hash=get_password_hash(refresh_token),
            expires_at=datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days),
        )
    )
    db.commit()

    return access_token, refresh_token


def _find_refresh_token_record(
    db: Session, raw_refresh_token: str
) -> Tuple[Optional[RefreshToken], Optional[dict]]:
    payload = decode_token(raw_refresh_token)
    if payload is None or not verify_token_type(payload, "refresh"):
        return None, None

    user_id = payload.get("sub")
    if not user_id:
        return None, None

    token_rows = (
        db.query(RefreshToken)
        .filter(
            RefreshToken.user_id == user_id,
            RefreshToken.is_deleted == False,
            RefreshToken.expires_at > datetime.utcnow(),
        )
        .all()
    )
    for row in token_rows:
        if verify_password(raw_refresh_token, row.refresh_token_hash):
            return row, payload

    return None, payload


@router.post("/login", response_model=StandardResponse)
async def login(
    login_data: LoginRequest,
    response: Response,
    db: Session = Depends(get_db),
):
    user = (
        db.query(User)
        .filter(User.email == login_data.email, User.is_deleted == False)
        .first()
    )
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token, refresh_token = _issue_tokens_for_user(user, db)
    _set_refresh_cookie(response, refresh_token)

    return StandardResponse(
        success=True,
        message="Login successful",
        data={
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "role": user.role.value,
            },
        },
    )


@router.post("/refresh", response_model=StandardResponse)
async def refresh_access_token(
    request: Request,
    response: Response,
    refresh_data: Optional[RefreshRequest] = None,
    db: Session = Depends(get_db),
):
    body_token = refresh_data.refresh_token if refresh_data else None
    cookie_token = request.cookies.get(REFRESH_COOKIE_NAME)
    raw_refresh_token = body_token or cookie_token

    if not raw_refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token is required",
        )

    token_row, payload = _find_refresh_token_record(db, raw_refresh_token)
    if token_row is None or payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

    user = (
        db.query(User)
        .filter(User.id == token_row.user_id, User.is_deleted == False)
        .first()
    )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    # Rotate refresh token: invalidate old record and issue a fresh one.
    token_row.is_deleted = True
    db.commit()

    access_token, new_refresh_token = _issue_tokens_for_user(user, db)
    _set_refresh_cookie(response, new_refresh_token)

    return StandardResponse(
        success=True,
        message="Token refreshed successfully",
        data={
            "access_token": access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer",
        },
    )


@router.post("/logout", response_model=StandardResponse)
async def logout(
    request: Request,
    response: Response,
    logout_data: Optional[LogoutRequest] = None,
    db: Session = Depends(get_db),
):
    body_token = logout_data.refresh_token if logout_data else None
    cookie_token = request.cookies.get(REFRESH_COOKIE_NAME)
    raw_refresh_token = body_token or cookie_token

    if raw_refresh_token:
        token_row, payload = _find_refresh_token_record(db, raw_refresh_token)
        if token_row is not None:
            token_row.is_deleted = True
            db.commit()
        elif payload and payload.get("sub"):
            # If token was decodable but hash lookup failed, revoke all active
            # refresh tokens for this user as a safe fallback.
            user_id = payload["sub"]
            (
                db.query(RefreshToken)
                .filter(
                    RefreshToken.user_id == user_id,
                    RefreshToken.is_deleted == False,
                )
                .update({"is_deleted": True})
            )
            db.commit()

    _clear_refresh_cookie(response)

    return StandardResponse(
        success=True,
        message="Logout successful",
        data=None,
    )


@router.post("/register", response_model=StandardResponse)
async def register_user(
    register_data: RegisterRequest,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
):
    _ = current_admin  # explicit: dependency enforces admin-only access

    existing_user = db.query(User).filter(User.email == register_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )

    role_value = register_data.role.lower()
    if role_value not in {UserRole.ADMIN.value, UserRole.CONTRIBUTOR.value}:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role must be either 'admin' or 'contributor'",
        )

    new_user = User(
        email=register_data.email,
        hashed_password=get_password_hash(register_data.password),
        role=UserRole(role_value),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return StandardResponse(
        success=True,
        message="User registered successfully",
        data={
            "id": new_user.id,
            "email": new_user.email,
            "role": new_user.role.value,
        },
    )


@router.get("/me", response_model=StandardResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return StandardResponse(
        success=True,
        message="Current user fetched successfully",
        data={
            "id": current_user.id,
            "email": current_user.email,
            "role": current_user.role.value,
        },
    )
