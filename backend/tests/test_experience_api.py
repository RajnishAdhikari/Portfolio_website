"""
Unit tests for Experience API endpoints.
Tests CRUD operations, file uploads, and authorization.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from io import BytesIO

from app.models.experience import Experience


class TestExperienceEndpoints:
    """Tests for experience CRUD endpoints."""
    
    def test_list_experiences_empty(self, client: TestClient):
        """Test listing experiences when none exist."""
        response = client.get("/api/v1/experience")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert len(data["data"]) == 0
    
    def test_create_experience_success(
        self, client: TestClient, admin_headers: dict, db_session: Session
    ):
        """Test creating a new experience entry."""
        experience_data = {
            "company": "Tech Corp",
            "position": "Senior Developer",
            "location": "San Francisco, CA",
            "employment_type": "Full-time",
            "start_month_year": "2020-01",
            "end_month_year": "2022-12",
            "description": "Led development of microservices"
        }
        
        response = client.post(
            "/api/v1/experience",
            json=experience_data,
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["company"] == "Tech Corp"
        assert data["data"]["position"] == "Senior Developer"
        assert data["data"]["location"] == "San Francisco, CA"
        
        # Verify in database
        exp = db_session.query(Experience).first()
        assert exp is not None
        assert exp.company == "Tech Corp"
    
    def test_create_experience_current_position(
        self, client: TestClient, admin_headers: dict
    ):
        """Test creating experience for current position (no end date)."""
        experience_data = {
            "company": "Current Co",
            "position": "Tech Lead",
            "start_month_year": "2023-01",
            "end_month_year": None
        }
        
        response = client.post(
            "/api/v1/experience",
            json=experience_data,
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["end_month_year"] is None
    
    def test_create_experience_without_auth(self, client: TestClient):
        """Test that creating experience requires authentication."""
        response = client.post(
            "/api/v1/experience",
            json={
                "company": "Test",
                "position": "Developer",
                "start_month_year": "2020-01"
            }
        )
        
        assert response.status_code == 401
    
    def test_create_experience_missing_required_fields(
        self, client: TestClient, admin_headers: dict
    ):
        """Test validation for required fields."""
        response = client.post(
            "/api/v1/experience",
            json={"company": "Test"},  # Missing position and start_month_year
            headers=admin_headers
        )
        
        assert response.status_code == 422
    
    def test_list_experiences_multiple(
        self, client: TestClient, admin_headers: dict, db_session: Session
    ):
        """Test listing multiple experiences."""
        experiences = [
            Experience(
                company="Company A",
                position="Developer",
                start_month_year="2018-01",
                end_month_year="2020-01"
            ),
            Experience(
                company="Company B",
                position="Senior Dev",
                start_month_year="2020-02",
                end_month_year="2022-01"
            ),
            Experience(
                company="Company C",
                position="Tech Lead",
                start_month_year="2022-02"
            )
        ]
        
        for exp in experiences:
            db_session.add(exp)
        db_session.commit()
        
        response = client.get("/api/v1/experience")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert len(data["data"]) == 3
    
    def test_update_experience_success(
        self, client: TestClient, admin_headers: dict, db_session: Session
    ):
        """Test updating an experience entry."""
        # Create experience
        exp = Experience(
            company="Old Company",
            position="Junior Dev",
            start_month_year="2019-01"
        )
        db_session.add(exp)
        db_session.commit()
        db_session.refresh(exp)
        
        # Update
        update_data = {
            "position": "Senior Developer",
            "end_month_year": "2021-12"
        }
        
        response = client.patch(
            f"/api/v1/experience/{exp.id}",
            json=update_data,
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["position"] == "Senior Developer"
        assert data["data"]["company"] == "Old Company"  # Unchanged
        assert data["data"]["end_month_year"] == "2021-12"
    
    def test_update_experience_not_found(
        self, client: TestClient, admin_headers: dict
    ):
        """Test updating non-existent experience."""
        response = client.patch(
            "/api/v1/experience/nonexistent-id",
            json={"position": "Updated"},
            headers=admin_headers
        )
        
        assert response.status_code == 404
    
    def test_update_experience_without_auth(
        self, client: TestClient, db_session: Session
    ):
        """Test that updating requires authentication."""
        exp = Experience(
            company="Test",
            position="Dev",
            start_month_year="2020-01"
        )
        db_session.add(exp)
        db_session.commit()
        db_session.refresh(exp)
        
        response = client.patch(
            f"/api/v1/experience/{exp.id}",
            json={"position": "Updated"}
        )
        
        assert response.status_code == 401
    
    def test_delete_experience_success(
        self, client: TestClient, admin_headers: dict, db_session: Session
    ):
        """Test soft deleting an experience."""
        exp = Experience(
            company="To Delete",
            position="Dev",
            start_month_year="2020-01"
        )
        db_session.add(exp)
        db_session.commit()
        db_session.refresh(exp)
        
        response = client.delete(
            f"/api/v1/experience/{exp.id}",
            headers=admin_headers
        )
        
        assert response.status_code == 200
        
        # Verify soft delete
        db_session.refresh(exp)
        assert exp.is_deleted is True
        
        # Verify not in list
        list_response = client.get("/api/v1/experience")
        assert len(list_response.json()["data"]) == 0
    
    def test_delete_experience_not_found(
        self, client: TestClient, admin_headers: dict
    ):
        """Test deleting non-existent experience."""
        response = client.delete(
            "/api/v1/experience/nonexistent-id",
            headers=admin_headers
        )
        
        assert response.status_code == 404
    
    def test_delete_experience_without_auth(
        self, client: TestClient, db_session: Session
    ):
        """Test that deleting requires authentication."""
        exp = Experience(
            company="Test",
            position="Dev",
            start_month_year="2020-01"
        )
        db_session.add(exp)
        db_session.commit()
        db_session.refresh(exp)
        
        response = client.delete(f"/api/v1/experience/{exp.id}")
        
        assert response.status_code == 401
    
    def test_upload_logo_success(
        self, client: TestClient, admin_headers: dict, db_session: Session
    ):
        """Test uploading a logo for experience."""
        # Create experience
        exp = Experience(
            company="Test Co",
            position="Dev",
            start_month_year="2020-01"
        )
        db_session.add(exp)
        db_session.commit()
        db_session.refresh(exp)
        
        # Create mock image file
        file_content = b"fake image content"
        files = {
            "file": ("logo.png", BytesIO(file_content), "image/png")
        }
        
        response = client.post(
            f"/api/v1/experience/{exp.id}/upload-logo",
            files=files,
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "file_path" in data["data"]
    
    def test_upload_logo_experience_not_found(
        self, client: TestClient, admin_headers: dict
    ):
        """Test uploading logo for non-existent experience."""
        file_content = b"fake image"
        files = {
            "file": ("logo.png", BytesIO(file_content), "image/png")
        }
        
        response = client.post(
            "/api/v1/experience/nonexistent-id/upload-logo",
            files=files,
            headers=admin_headers
        )
        
        assert response.status_code == 404
