"""
Pytest Configuration and Fixtures
================================

This module defines global pytest fixtures and configuration for the test suite.
It sets up an isolated in-memory SQLite database for each test to ensure
no side effects between tests.

Key Features:
    - In-memory SQLite database (fast, no cleanup needed)
    - Fresh database for EVERY test function
    - Test client with database dependency overrides
    - Pre-configured admin and regular user fixtures
    - Authentication token fixtures

Usage:
    def test_example(client, db_session, admin_headers):
        # Fixtures are automatically injected by pytest
        pass
"""

import pytest
from typing import Generator, Dict, Any
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.models.user import User, UserRole
from app.models.refresh_token import RefreshToken
from app.models.personal import Personal
from app.models.education import Education
from app.models.experience import Experience
from app.models.skill import Skill
from app.models.project import Project
from app.models.article import Article
from app.models.certification import Certification
from app.models.extracurricular import Extracurricular
from app.models.resource_paper import ResourcePaper
from app.core.security import get_password_hash, create_access_token


# ============================================================================
# DATABASE SETUP
# ============================================================================

# Use in-memory SQLite for fastest possible tests
# check_same_thread=False is needed because FastAPI runs in a separate thread
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # Use single connection pool for in-memory DB
)

TestingSessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)


# ============================================================================
# SESSION FIXTURES
# ============================================================================

@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    """
    Create a fresh database session for a test.
    
    This fixture:
    1. Creates all tables in the in-memory database
    2. Yields a session
    3. Drops all tables after the test finishes
    
    Scope: function (runs for every single test)
    """
    # Create schema
    Base.metadata.create_all(bind=engine)
    
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        # Clean up schema
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """
    Create a TestClient with overridden database dependency.
    
    This ensures the API uses our in-memory test database instead of
    the real database defined in app.database.
    """
    
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    # Override the get_db dependency
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Clean up overrides
    app.dependency_overrides.clear()


# ============================================================================
# USER FIXTURES
# ============================================================================

@pytest.fixture(scope="function")
def test_admin(db_session: Session) -> User:
    """
    Create and return a test admin user.
    """
    admin = User(
        email="testadmin@example.com",
        hashed_password=get_password_hash("TestAdmin123!"),
        role=UserRole.ADMIN
    )
    db_session.add(admin)
    db_session.commit()
    db_session.refresh(admin)
    return admin


@pytest.fixture(scope="function")
def test_user(db_session: Session) -> User:
    """
    Create and return a test contributor user.
    """
    user = User(
        email="testuser@example.com",
        hashed_password=get_password_hash("TestUser123!"),
        role=UserRole.CONTRIBUTOR
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


# ============================================================================
# AUTHENTICATION FIXTURES
# ============================================================================

@pytest.fixture(scope="function")
def admin_token(test_admin: User) -> str:
    """
    Generate a valid JWT access token for the admin user.
    """
    token = create_access_token(
        data={"sub": test_admin.id, "role": test_admin.role.value}
    )
    return token


@pytest.fixture(scope="function")
def admin_headers(admin_token: str) -> Dict[str, str]:
    """
    Return Authorization headers for admin requests.
    
    Usage:
        client.get("/protected", headers=admin_headers)
    """
    return {"Authorization": f"Bearer {admin_token}"}
