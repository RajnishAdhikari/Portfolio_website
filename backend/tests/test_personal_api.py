"""
Personal Info API Tests
======================

This module tests the Personal Info API endpoints.
Verifies public read access and admin-only write access.

Routes:
    - GET /api/v1/personal
    - PATCH /api/v1/personal
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.personal import Personal


class TestPersonalEndpoints:
    """
    Tests for personal info CRUD operations.
    """
    
    # ========================================================================
    # READ TESTS
    # ========================================================================
    
    def test_get_personal_info_empty(self, client: TestClient):
        """
        Test getting personal info when none exists.
        Should return success with null/empty data.
        """
        response = client.get("/api/v1/personal")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
    
    def test_get_personal_info_with_data(
        self, client: TestClient, db_session: Session
    ):
        """
        Test getting personal info when data exists.
        Should return the personal info object.
        """
        # Create personal info
        personal = Personal(
            full_name="John Doe",
            tagline="Full Stack Developer",
            email="john@example.com",
            github_url="https://github.com/johndoe"
        )
        db_session.add(personal)
        db_session.commit()
        
        response = client.get("/api/v1/personal")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["full_name"] == "John Doe"
    
    # ========================================================================
    # UPDATE TESTS
    # ========================================================================
    
    def test_update_personal_info(
        self, client: TestClient, admin_headers: dict, db_session: Session
    ):
        """
        Test updating personal info as admin.
        Should update fields and return updated object.
        """
        # Create initial personal info
        personal = Personal(full_name="Old Name")
        db_session.add(personal)
        db_session.commit()
        
        response = client.patch(
            "/api/v1/personal",
            json={
                "full_name": "New Name",
                "tagline": "Updated Tagline",
                "linkedin_url": "https://linkedin.com/in/newname"
            },
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["full_name"] == "New Name"
        assert data["data"]["tagline"] == "Updated Tagline"
    
    def test_update_personal_info_unauthorized(self, client: TestClient):
        """
        Test updating personal info without authentication.
        Should return 401 Unauthorized.
        """
        response = client.patch(
            "/api/v1/personal",
            json={"full_name": "Unauthorized Update"}
        )
        
        assert response.status_code == 401
    
    def test_update_personal_partial(
        self, client: TestClient, admin_headers: dict, db_session: Session
    ):
        """
        Test partial update of personal info.
        Only specified fields should change.
        """
        # Create initial personal info with multiple fields
        personal = Personal(
            full_name="John Doe",
            tagline="Developer",
            email="john@example.com"
        )
        db_session.add(personal)
        db_session.commit()
        
        # Update only tagline
        response = client.patch(
            "/api/v1/personal",
            json={"tagline": "Senior Developer"},
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        # Tagline should be updated
        assert data["data"]["tagline"] == "Senior Developer"
        # Other fields should remain unchanged
        assert data["data"]["full_name"] == "John Doe"


class TestPersonalInfoValidation:
    """
    Tests for personal info input validation.
    """
    
    def test_update_with_valid_urls(
        self, client: TestClient, admin_headers: dict, db_session: Session
    ):
        """
        Test updating with valid URL fields.
        """
        personal = Personal(full_name="Test")
        db_session.add(personal)
        db_session.commit()
        
        response = client.patch(
            "/api/v1/personal",
            json={
                "github_url": "https://github.com/test",
                "linkedin_url": "https://linkedin.com/in/test",
                "twitter_url": "https://twitter.com/test"
            },
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["github_url"] == "https://github.com/test"
