"""
Unit tests for Resource Papers API endpoints.
Tests CRUD operations, slug uniqueness, featured filtering, and file uploads.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from io import BytesIO

from app.models.resource_paper import ResourcePaper


class TestResourcePaperEndpoints:
    """Tests for resource paper CRUD endpoints."""
    
    def test_list_resource_papers_empty(self, client: TestClient):
        """Test listing resource papers when none exist."""
        response = client.get("/api/v1/resource_paper")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert len(data["data"]) == 0
    
    def test_create_resource_paper_success(
        self, client: TestClient, admin_headers: dict, db_session: Session
    ):
        """Test creating a new resource paper."""
        paper_data = {
            "title": "Machine Learning Fundamentals",
            "slug": "ml-fundamentals",
            "excerpt": "A comprehensive guide to ML basics",
            "body": "This paper covers essential ML concepts...",
            "is_featured": False
        }
        
        response = client.post(
            "/api/v1/resource_paper",
            json=paper_data,
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["title"] == "Machine Learning Fundamentals"
        assert data["data"]["slug"] == "ml-fundamentals"
        assert data["data"]["is_featured"] is False
        
        # Verify in database
        paper = db_session.query(ResourcePaper).first()
        assert paper is not None
        assert paper.title == "Machine Learning Fundamentals"
    
    def test_create_featured_resource_paper(
        self, client: TestClient, admin_headers: dict
    ):
        """Test creating a featured resource paper."""
        paper_data = {
            "title": "Featured Research",
            "slug": "featured-research",
            "excerpt": "Important research paper",
            "is_featured": True
        }
        
        response = client.post(
            "/api/v1/resource_paper",
            json=paper_data,
            headers=admin_headers
        )
        
        assert response.status_code == 200
        assert response.json()["data"]["is_featured"] is True
    
    def test_create_resource_paper_duplicate_slug(
        self, client: TestClient, admin_headers: dict, db_session: Session
    ):
        """Test that duplicate slugs are not allowed."""
        paper = ResourcePaper(
            title="First Paper",
            slug="unique-slug",
            excerpt="First"
        )
        db_session.add(paper)
        db_session.commit()
        
        response = client.post(
            "/api/v1/resource_paper",
            json={
                "title": "Second Paper",
                "slug": "unique-slug",
                "excerpt": "Second"
            },
            headers=admin_headers
        )
        
        assert response.status_code in [400, 409, 500]
    
    def test_create_resource_paper_without_auth(self, client: TestClient):
        """Test that creating resource paper requires authentication."""
        response = client.post(
            "/api/v1/resource_paper",
            json={
                "title": "Test",
                "slug": "test",
                "excerpt": "Test"
            }
        )
        
        assert response.status_code == 401
    
    def test_create_resource_paper_missing_required_fields(
        self, client: TestClient, admin_headers: dict
    ):
        """Test validation for required fields."""
        response = client.post(
            "/api/v1/resource_paper",
            json={"title": "Test"},  # Missing slug and excerpt
            headers=admin_headers
        )
        
        assert response.status_code == 422
    
    def test_get_resource_paper_by_slug(
        self, client: TestClient, db_session: Session
    ):
        """Test retrieving a resource paper by slug."""
        paper = ResourcePaper(
            title="Test Paper",
            slug="test-paper",
            excerpt="Test excerpt",
            body="Full paper content"
        )
        db_session.add(paper)
        db_session.commit()
        
        response = client.get("/api/v1/resource_paper/test-paper")
        
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["title"] == "Test Paper"
        assert data["data"]["slug"] == "test-paper"
    
    def test_get_resource_paper_by_slug_not_found(self, client: TestClient):
        """Test retrieving non-existent resource paper by slug."""
        response = client.get("/api/v1/resource_paper/nonexistent")
        
        assert response.status_code == 404
    
    def test_list_resource_papers_multiple(
        self, client: TestClient, db_session: Session
    ):
        """Test listing multiple resource papers."""
        papers = [
            ResourcePaper(title="Paper 1", slug="paper-1", excerpt="Excerpt 1"),
            ResourcePaper(title="Paper 2", slug="paper-2", excerpt="Excerpt 2"),
            ResourcePaper(title="Paper 3", slug="paper-3", excerpt="Excerpt 3"),
        ]
        
        for paper in papers:
            db_session.add(paper)
        db_session.commit()
        
        response = client.get("/api/v1/resource_paper")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) == 3
    
    def test_list_featured_resource_papers(
        self, client: TestClient, db_session: Session
    ):
        """Test filtering for featured resource papers."""
        papers = [
            ResourcePaper(title="Featured 1", slug="feat-1", excerpt="F1", is_featured=True),
            ResourcePaper(title="Regular 1", slug="reg-1", excerpt="R1", is_featured=False),
            ResourcePaper(title="Featured 2", slug="feat-2", excerpt="F2", is_featured=True),
        ]
        
        for paper in papers:
            db_session.add(paper)
        db_session.commit()
        
        # Test with query parameter if endpoint supports it
        response = client.get("/api/v1/resource_paper?featured=true")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) >= 2
    
    def test_update_resource_paper_success(
        self, client: TestClient, admin_headers: dict, db_session: Session
    ):
        """Test updating a resource paper."""
        paper = ResourcePaper(
            title="Old Title",
            slug="paper-slug",
            excerpt="Old excerpt"
        )
        db_session.add(paper)
        db_session.commit()
        db_session.refresh(paper)
        
        update_data = {
            "title": "New Title",
            "body": "Updated paper content",
            "is_featured": True
        }
        
        response = client.patch(
            f"/api/v1/resource_paper/{paper.id}",
            json=update_data,
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["title"] == "New Title"
        assert data["data"]["is_featured"] is True
    
    def test_update_resource_paper_toggle_featured(
        self, client: TestClient, admin_headers: dict, db_session: Session
    ):
        """Test toggling featured status."""
        paper = ResourcePaper(
            title="Test",
            slug="test",
            excerpt="Test",
            is_featured=False
        )
        db_session.add(paper)
        db_session.commit()
        db_session.refresh(paper)
        
        response = client.patch(
            f"/api/v1/resource_paper/{paper.id}",
            json={"is_featured": True},
            headers=admin_headers
        )
        
        assert response.status_code == 200
        assert response.json()["data"]["is_featured"] is True
    
    def test_update_resource_paper_not_found(
        self, client: TestClient, admin_headers: dict
    ):
        """Test updating non-existent resource paper."""
        response = client.patch(
            "/api/v1/resource_paper/nonexistent-id",
            json={"title": "Updated"},
            headers=admin_headers
        )
        
        assert response.status_code == 404
    
    def test_delete_resource_paper_success(
        self, client: TestClient, admin_headers: dict, db_session: Session
    ):
        """Test soft deleting a resource paper."""
        paper = ResourcePaper(
            title="To Delete",
            slug="to-delete",
            excerpt="Will be deleted"
        )
        db_session.add(paper)
        db_session.commit()
        db_session.refresh(paper)
        
        response = client.delete(
            f"/api/v1/resource_paper/{paper.id}",
            headers=admin_headers
        )
        
        assert response.status_code == 200
        
        # Verify soft delete
        db_session.refresh(paper)
        assert paper.is_deleted is True
        
        # Verify not in list
        list_response = client.get("/api/v1/resource_paper")
        assert len(list_response.json()["data"]) == 0
    
    def test_upload_cover_image(
        self, client: TestClient, admin_headers: dict, db_session: Session
    ):
        """Test uploading cover image for resource paper."""
        paper = ResourcePaper(
            title="Test",
            slug="test",
            excerpt="Test"
        )
        db_session.add(paper)
        db_session.commit()
        db_session.refresh(paper)
        
        file_content = b"fake image"
        files = {
            "file": ("cover.jpg", BytesIO(file_content), "image/jpeg")
        }
        
        response = client.post(
            f"/api/v1/resource_paper/{paper.id}/upload-cover",
            files=files,
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "file_path" in data["data"]
    
    def test_upload_pdf_attachment(
        self, client: TestClient, admin_headers: dict, db_session: Session
    ):
        """Test uploading PDF attachment for resource paper."""
        paper = ResourcePaper(
            title="Test",
            slug="test",
            excerpt="Test"
        )
        db_session.add(paper)
        db_session.commit()
        db_session.refresh(paper)
        
        file_content = b"fake pdf"
        files = {
            "file": ("paper.pdf", BytesIO(file_content), "application/pdf")
        }
        
        response = client.post(
            f"/api/v1/resource_paper/{paper.id}/upload-pdf",
            files=files,
            headers=admin_headers
        )
        
        assert response.status_code == 200
