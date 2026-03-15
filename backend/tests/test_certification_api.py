"""
Unit tests for Certifications API endpoints.
Tests CRUD operations, date validation, and file uploads.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from io import BytesIO

from app.models.certification import Certification


class TestCertificationEndpoints:
    """Tests for certification CRUD endpoints."""
    
    def test_list_certifications_empty(self, client: TestClient):
        """Test listing certifications when none exist."""
        response = client.get("/api/v1/certification")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert len(data["data"]) == 0
    
    def test_create_certification_success(
        self, client: TestClient, admin_headers: dict, db_session: Session
    ):
        """Test creating a new certification."""
        cert_data = {
            "name": "AWS Certified Solutions Architect",
            "issuer": "Amazon Web Services",
            "issue_month_year": "2023-06",
            "cred_id": "ABC123XYZ",
            "cred_url": "https://aws.amazon.com/verify/ABC123",
            "description": "Professional level certification"
        }
        
        response = client.post(
            "/api/v1/certification",
            json=cert_data,
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["name"] == "AWS Certified Solutions Architect"
        assert data["data"]["issuer"] == "Amazon Web Services"
        assert data["data"]["cred_id"] == "ABC123XYZ"
        
        # Verify in database
        cert = db_session.query(Certification).first()
        assert cert is not None
        assert cert.name == "AWS Certified Solutions Architect"
    
    def test_create_certification_minimal(
        self, client: TestClient, admin_headers: dict
    ):
        """Test creating certification with minimal required fields."""
        cert_data = {
            "name": "Basic Cert",
            "issuer": "Test Org",
            "issue_month_year": "2023-01"
        }
        
        response = client.post(
            "/api/v1/certification",
            json=cert_data,
            headers=admin_headers
        )
        
        assert response.status_code == 200
        assert response.json()["data"]["name"] == "Basic Cert"
    
    def test_create_certification_without_auth(self, client: TestClient):
        """Test that creating certification requires authentication."""
        response = client.post(
            "/api/v1/certification",
            json={
                "name": "Test",
                "issuer": "Test",
                "issue_month_year": "2023-01"
            }
        )
        
        assert response.status_code == 401
    
    def test_create_certification_missing_required_fields(
        self, client: TestClient, admin_headers: dict
    ):
        """Test validation for required fields."""
        response = client.post(
            "/api/v1/certification",
            json={"name": "Test"},  # Missing issuer and issue_month_year
            headers=admin_headers
        )
        
        assert response.status_code == 422
    
    def test_list_certifications_multiple(
        self, client: TestClient, db_session: Session
    ):
        """Test listing multiple certifications."""
        certs = [
            Certification(
                name="Cert 1",
                issuer="Issuer A",
                issue_month_year="2021-01"
            ),
            Certification(
                name="Cert 2",
                issuer="Issuer B",
                issue_month_year="2022-06"
            ),
            Certification(
                name="Cert 3",
                issuer="Issuer C",
                issue_month_year="2023-12"
            ),
        ]
        
        for cert in certs:
            db_session.add(cert)
        db_session.commit()
        
        response = client.get("/api/v1/certification")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) == 3
    
    def test_update_certification_success(
        self, client: TestClient, admin_headers: dict, db_session: Session
    ):
        """Test updating a certification."""
        cert = Certification(
            name="Old Cert Name",
            issuer="Old Issuer",
            issue_month_year="2020-01"
        )
        db_session.add(cert)
        db_session.commit()
        db_session.refresh(cert)
        
        update_data = {
            "name": "New Cert Name",
            "cred_id": "NEW123",
            "cred_url": "https://example.com/verify"
        }
        
        response = client.patch(
            f"/api/v1/certification/{cert.id}",
            json=update_data,
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["name"] == "New Cert Name"
        assert data["data"]["issuer"] == "Old Issuer"  # Unchanged
        assert data["data"]["cred_id"] == "NEW123"
    
    def test_update_certification_not_found(
        self, client: TestClient, admin_headers: dict
    ):
        """Test updating non-existent certification."""
        response = client.patch(
            "/api/v1/certification/nonexistent-id",
            json={"name": "Updated"},
            headers=admin_headers
        )
        
        assert response.status_code == 404
    
    def test_update_certification_without_auth(
        self, client: TestClient, db_session: Session
    ):
        """Test that updating requires authentication."""
        cert = Certification(
            name="Test",
            issuer="Test",
            issue_month_year="2023-01"
        )
        db_session.add(cert)
        db_session.commit()
        db_session.refresh(cert)
        
        response = client.patch(
            f"/api/v1/certification/{cert.id}",
            json={"name": "Updated"}
        )
        
        assert response.status_code == 401
    
    def test_delete_certification_success(
        self, client: TestClient, admin_headers: dict, db_session: Session
    ):
        """Test soft deleting a certification."""
        cert = Certification(
            name="To Delete",
            issuer="Test",
            issue_month_year="2023-01"
        )
        db_session.add(cert)
        db_session.commit()
        db_session.refresh(cert)
        
        response = client.delete(
            f"/api/v1/certification/{cert.id}",
            headers=admin_headers
        )
        
        assert response.status_code == 200
        
        # Verify soft delete
        db_session.refresh(cert)
        assert cert.is_deleted is True
        
        # Verify not in list
        list_response = client.get("/api/v1/certification")
        assert len(list_response.json()["data"]) == 0
    
    def test_delete_certification_not_found(
        self, client: TestClient, admin_headers: dict
    ):
        """Test deleting non-existent certification."""
        response = client.delete(
            "/api/v1/certification/nonexistent-id",
            headers=admin_headers
        )
        
        assert response.status_code == 404
    
    def test_delete_certification_without_auth(
        self, client: TestClient, db_session: Session
    ):
        """Test that deleting requires authentication."""
        cert = Certification(
            name="Test",
            issuer="Test",
            issue_month_year="2023-01"
        )
        db_session.add(cert)
        db_session.commit()
        db_session.refresh(cert)
        
        response = client.delete(f"/api/v1/certification/{cert.id}")
        
        assert response.status_code == 401
    
    def test_upload_certificate_image(
        self, client: TestClient, admin_headers: dict, db_session: Session
    ):
        """Test uploading certificate image."""
        cert = Certification(
            name="Test",
            issuer="Test",
            issue_month_year="2023-01"
        )
        db_session.add(cert)
        db_session.commit()
        db_session.refresh(cert)
        
        file_content = b"fake certificate image"
        files = {
            "file": ("cert.jpg", BytesIO(file_content), "image/jpeg")
        }
        
        response = client.post(
            f"/api/v1/certification/{cert.id}/upload-image",
            files=files,
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "file_path" in data["data"]
    
    def test_certification_date_format(
        self, client: TestClient, admin_headers: dict
    ):
        """Test that certification dates are in YYYY-MM format."""
        cert_data = {
            "name": "Test Cert",
            "issuer": "Test",
            "issue_month_year": "2023-06"
        }
        
        response = client.post(
            "/api/v1/certification",
            json=cert_data,
            headers=admin_headers
        )
        
        assert response.status_code == 200
        assert response.json()["data"]["issue_month_year"] == "2023-06"
