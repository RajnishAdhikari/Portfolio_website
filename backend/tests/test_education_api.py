"""
Unit tests for Education API endpoints.
Tests full CRUD operations for education entries.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.education import Education


class TestEducationEndpoints:
    """Tests for education CRUD endpoints."""
    
    def test_list_education_empty(self, client: TestClient):
        """Test listing education with no entries."""
        response = client.get("/api/v1/education")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert data["data"] == []
    
    def test_create_education(self, client: TestClient, admin_headers: dict):
        """Test creating a new education entry."""
        education_data = {
            "institution": "Harvard University",
            "degree": "Master of Science",
            "field": "Computer Science",
            "location": "Cambridge, MA",
            "grade": "4.0 GPA",
            "start_month_year": "2020-09",
            "end_month_year": "2022-05",
            "description": "Focused on distributed systems"
        }
        
        response = client.post(
            "/api/v1/education",
            json=education_data,
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert data["data"]["institution"] == "Harvard University"
        assert data["data"]["degree"] == "Master of Science"
        assert "id" in data["data"]
    
    def test_create_education_minimal(self, client: TestClient, admin_headers: dict):
        """Test creating education with minimal required fields."""
        education_data = {
            "institution": "MIT",
            "degree": "PhD",
            "start_month_year": "2022-09"
        }
        
        response = client.post(
            "/api/v1/education",
            json=education_data,
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["institution"] == "MIT"
    
    def test_create_education_unauthorized(self, client: TestClient):
        """Test creating education without authentication."""
        response = client.post(
            "/api/v1/education",
            json={
                "institution": "Test",
                "degree": "BS",
                "start_month_year": "2020-09"
            }
        )
        
        assert response.status_code == 401
    
    def test_update_education(
        self, client: TestClient, admin_headers: dict, db_session: Session
    ):
        """Test updating an existing education entry."""
        # Create an education entry first
        education = Education(
            institution="Old University",
            degree="BS",
            start_month_year="2020-09"
        )
        db_session.add(education)
        db_session.commit()
        db_session.refresh(education)
        
        # Update it
        response = client.patch(
            f"/api/v1/education/{education.id}",
            json={
                "institution": "New University",
                "degree": "Master of Science"
            },
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["institution"] == "New University"
        assert data["data"]["degree"] == "Master of Science"
    
    def test_update_education_not_found(self, client: TestClient, admin_headers: dict):
        """Test updating non-existent education entry."""
        response = client.patch(
            "/api/v1/education/nonexistent-id",
            json={"institution": "Test"},
            headers=admin_headers
        )
        
        assert response.status_code == 404
    
    def test_delete_education(
        self, client: TestClient, admin_headers: dict, db_session: Session
    ):
        """Test soft deleting an education entry."""
        # Create an education entry first
        education = Education(
            institution="Delete Me University",
            degree="BS",
            start_month_year="2020-09"
        )
        db_session.add(education)
        db_session.commit()
        db_session.refresh(education)
        
        # Delete it
        response = client.delete(
            f"/api/v1/education/{education.id}",
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        
        # Verify it's soft deleted (not in list)
        list_response = client.get("/api/v1/education")
        assert all(
            edu["id"] != education.id 
            for edu in list_response.json()["data"]
        )
    
    def test_delete_education_not_found(self, client: TestClient, admin_headers: dict):
        """Test deleting non-existent education entry."""
        response = client.delete(
            "/api/v1/education/nonexistent-id",
            headers=admin_headers
        )
        
        assert response.status_code == 404
    
    def test_list_education_after_create(
        self, client: TestClient, admin_headers: dict
    ):
        """Test that created education appears in list."""
        # Create education
        client.post(
            "/api/v1/education",
            json={
                "institution": "Test University",
                "degree": "BS",
                "start_month_year": "2020-09"
            },
            headers=admin_headers
        )
        
        # List should now include it
        response = client.get("/api/v1/education")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) >= 1
        assert any(
            edu["institution"] == "Test University" 
            for edu in data["data"]
        )
