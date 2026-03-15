"""
Unit tests for Extracurricular API endpoints.
Tests CRUD operations, optional fields, and file uploads.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from io import BytesIO

from app.models.extracurricular import Extracurricular


class TestExtracurricularEndpoints:
    """Tests for extracurricular CRUD endpoints."""
    
    def test_list_extracurriculars_empty(self, client: TestClient):
        """Test listing extracurriculars when none exist."""
        response = client.get("/api/v1/extracurricular")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert len(data["data"]) == 0
    
    def test_create_extracurricular_success(
        self, client: TestClient, admin_headers: dict, db_session: Session
    ):
        """Test creating a new extracurricular activity."""
        extra_data = {
            "title": "Volunteer at Animal Shelter",
            "organisation": "City Animal Shelter",
            "start_month_year": "2022-01",
            "end_month_year": "2023-12",
            "description": "Volunteered weekly to help care for animals",
            "external_url": "https://shelter.org"
        }
        
        response = client.post(
            "/api/v1/extracurricular",
            json=extra_data,
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["title"] == "Volunteer at Animal Shelter"
        assert data["data"]["organisation"] == "City Animal Shelter"
        
        # Verify in database
        extra = db_session.query(Extracurricular).first()
        assert extra is not None
        assert extra.title == "Volunteer at Animal Shelter"
    
    def test_create_extracurricular_minimal(
        self, client: TestClient, admin_headers: dict
    ):
        """Test creating extracurricular with only title."""
        extra_data = {
            "title": "Community Service"
        }
        
        response = client.post(
            "/api/v1/extracurricular",
            json=extra_data,
            headers=admin_headers
        )
        
        assert response.status_code == 200
        assert response.json()["data"]["title"] == "Community Service"
    
    def test_create_extracurricular_ongoing(
        self, client: TestClient, admin_headers: dict
    ):
        """Test creating ongoing extracurricular (no end date)."""
        extra_data = {
            "title": "Ongoing Volunteer Work",
            "organisation": "Local Charity",
            "start_month_year": "2023-01",
            "end_month_year": None
        }
        
        response = client.post(
            "/api/v1/extracurricular",
            json=extra_data,
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["end_month_year"] is None
    
    def test_create_extracurricular_without_auth(self, client: TestClient):
        """Test that creating extracurricular requires authentication."""
        response = client.post(
            "/api/v1/extracurricular",
            json={"title": "Test Activity"}
        )
        
        assert response.status_code == 401
    
    def test_create_extracurricular_missing_title(
        self, client: TestClient, admin_headers: dict
    ):
        """Test validation for required title field."""
        response = client.post(
            "/api/v1/extracurricular",
            json={"organisation": "Test"},  # Missing title
            headers=admin_headers
        )
        
        assert response.status_code == 422
    
    def test_list_extracurriculars_multiple(
        self, client: TestClient, db_session: Session
    ):
        """Test listing multiple extracurricular activities."""
        extras = [
            Extracurricular(
                title="Activity 1",
                organisation="Org A",
                start_month_year="2021-01"
            ),
            Extracurricular(
                title="Activity 2",
                organisation="Org B",
                start_month_year="2022-06"
            ),
            Extracurricular(
                title="Activity 3"
            ),
        ]
        
        for extra in extras:
            db_session.add(extra)
        db_session.commit()
        
        response = client.get("/api/v1/extracurricular")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) == 3
    
    def test_update_extracurricular_success(
        self, client: TestClient, admin_headers: dict, db_session: Session
    ):
        """Test updating an extracurricular activity."""
        extra = Extracurricular(
            title="Old Title",
            organisation="Old Org"
        )
        db_session.add(extra)
        db_session.commit()
        db_session.refresh(extra)
        
        update_data = {
            "title": "New Title",
            "description": "Updated description",
            "end_month_year": "2023-12"
        }
        
        response = client.patch(
            f"/api/v1/extracurricular/{extra.id}",
            json=update_data,
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["title"] == "New Title"
        assert data["data"]["organisation"] == "Old Org"  # Unchanged
        assert data["data"]["end_month_year"] == "2023-12"
    
    def test_update_extracurricular_not_found(
        self, client: TestClient, admin_headers: dict
    ):
        """Test updating non-existent extracurricular."""
        response = client.patch(
            "/api/v1/extracurricular/nonexistent-id",
            json={"title": "Updated"},
            headers=admin_headers
        )
        
        assert response.status_code == 404
    
    def test_update_extracurricular_without_auth(
        self, client: TestClient, db_session: Session
    ):
        """Test that updating requires authentication."""
        extra = Extracurricular(title="Test")
        db_session.add(extra)
        db_session.commit()
        db_session.refresh(extra)
        
        response = client.patch(
            f"/api/v1/extracurricular/{extra.id}",
            json={"title": "Updated"}
        )
        
        assert response.status_code == 401
    
    def test_delete_extracurricular_success(
        self, client: TestClient, admin_headers: dict, db_session: Session
    ):
        """Test soft deleting an extracurricular."""
        extra = Extracurricular(title="To Delete")
        db_session.add(extra)
        db_session.commit()
        db_session.refresh(extra)
        
        response = client.delete(
            f"/api/v1/extracurricular/{extra.id}",
            headers=admin_headers
        )
        
        assert response.status_code == 200
        
        # Verify soft delete
        db_session.refresh(extra)
        assert extra.is_deleted is True
        
        # Verify not in list
        list_response = client.get("/api/v1/extracurricular")
        assert len(list_response.json()["data"]) == 0
    
    def test_delete_extracurricular_not_found(
        self, client: TestClient, admin_headers: dict
    ):
        """Test deleting non-existent extracurricular."""
        response = client.delete(
            "/api/v1/extracurricular/nonexistent-id",
            headers=admin_headers
        )
        
        assert response.status_code == 404
    
    def test_delete_extracurricular_without_auth(
        self, client: TestClient, db_session: Session
    ):
        """Test that deleting requires authentication."""
        extra = Extracurricular(title="Test")
        db_session.add(extra)
        db_session.commit()
        db_session.refresh(extra)
        
        response = client.delete(f"/api/v1/extracurricular/{extra.id}")
        
        assert response.status_code == 401
    
    def test_upload_certificate_image(
        self, client: TestClient, admin_headers: dict, db_session: Session
    ):
        """Test uploading certificate/achievement image."""
        extra = Extracurricular(title="Test Activity")
        db_session.add(extra)
        db_session.commit()
        db_session.refresh(extra)
        
        file_content = b"fake certificate"
        files = {
            "file": ("cert.png", BytesIO(file_content), "image/png")
        }
        
        response = client.post(
            f"/api/v1/extracurricular/{extra.id}/upload-certificate",
            files=files,
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "file_path" in data["data"]
    
    def test_extracurricular_with_external_url(
        self, client: TestClient, admin_headers: dict
    ):
        """Test creating extracurricular with external URL."""
        extra_data = {
            "title": "Hackathon Winner",
            "organisation": "Tech Hackathon 2023",
            "external_url": "https://hackathon2023.com/winners"
        }
        
        response = client.post(
            "/api/v1/extracurricular",
            json=extra_data,
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["external_url"] == "https://hackathon2023.com/winners"
