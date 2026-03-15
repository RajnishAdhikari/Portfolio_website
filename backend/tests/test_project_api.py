"""
Unit tests for Projects API endpoints.
Tests CRUD operations, slug uniqueness, file uploads, and JSON fields.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from io import BytesIO

from app.models.project import Project


class TestProjectEndpoints:
    """Tests for project CRUD endpoints."""
    
    def test_list_projects_empty(self, client: TestClient):
        """Test listing projects when none exist."""
        response = client.get("/api/v1/project")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert len(data["data"]) == 0
    
    def test_create_project_success(
        self, client: TestClient, admin_headers: dict, db_session: Session
    ):
        """Test creating a new project."""
        project_data = {
            "title": "E-commerce Platform",
            "slug": "ecommerce-platform",
            "short_desc": "A full-stack e-commerce solution",
            "detailed_desc": "Comprehensive e-commerce platform with React and FastAPI",
            "tech_stack": ["React", "FastAPI", "PostgreSQL", "Docker"],
            "external_url": "https://example.com",
            "github_url": "https://github.com/user/project"
        }
        
        response = client.post(
            "/api/v1/project",
            json=project_data,
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["title"] == "E-commerce Platform"
        assert data["data"]["slug"] == "ecommerce-platform"
        assert len(data["data"]["tech_stack"]) == 4
        
        # Verify in database
        project = db_session.query(Project).first()
        assert project is not None
        assert project.title == "E-commerce Platform"
    
    def test_create_project_minimal(
        self, client: TestClient, admin_headers: dict
    ):
        """Test creating project with minimal required fields."""
        project_data = {
            "title": "Simple Project",
            "slug": "simple-project",
            "short_desc": "A simple project"
        }
        
        response = client.post(
            "/api/v1/project",
            json=project_data,
            headers=admin_headers
        )
        
        assert response.status_code == 200
        assert response.json()["data"]["title"] == "Simple Project"
    
    def test_create_project_duplicate_slug(
        self, client: TestClient, admin_headers: dict, db_session: Session
    ):
        """Test that duplicate slugs are not allowed."""
        # Create first project
        project = Project(
            title="First Project",
            slug="unique-slug",
            short_desc="First"
        )
        db_session.add(project)
        db_session.commit()
        
        # Try to create second with same slug
        response = client.post(
            "/api/v1/project",
            json={
                "title": "Second Project",
                "slug": "unique-slug",
                "short_desc": "Second"
            },
            headers=admin_headers
        )
        
        # Should fail due to unique constraint
        assert response.status_code in [400, 409, 500]  # Various ways to handle duplicate
    
    def test_create_project_without_auth(self, client: TestClient):
        """Test that creating project requires authentication."""
        response = client.post(
            "/api/v1/project",
            json={
                "title": "Test",
                "slug": "test",
                "short_desc": "Test"
            }
        )
        
        assert response.status_code == 401
    
    def test_create_project_missing_required_fields(
        self, client: TestClient, admin_headers: dict
    ):
        """Test validation for required fields."""
        response = client.post(
            "/api/v1/project",
            json={"title": "Test"},  # Missing slug and short_desc
            headers=admin_headers
        )
        
        assert response.status_code == 422
    
    def test_get_project_by_slug(
        self, client: TestClient, db_session: Session
    ):
        """Test retrieving a project by slug."""
        project = Project(
            title="Test Project",
            slug="test-project",
            short_desc="A test project",
            tech_stack=["Python", "FastAPI"]
        )
        db_session.add(project)
        db_session.commit()
        
        response = client.get("/api/v1/project/test-project")
        
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["title"] == "Test Project"
        assert data["data"]["slug"] == "test-project"
    
    def test_get_project_by_slug_not_found(self, client: TestClient):
        """Test retrieving non-existent project by slug."""
        response = client.get("/api/v1/project/nonexistent-slug")
        
        assert response.status_code == 404
    
    def test_list_projects_multiple(
        self, client: TestClient, db_session: Session
    ):
        """Test listing multiple projects."""
        projects = [
            Project(title="Project A", slug="project-a", short_desc="A"),
            Project(title="Project B", slug="project-b", short_desc="B"),
            Project(title="Project C", slug="project-c", short_desc="C"),
        ]
        
        for project in projects:
            db_session.add(project)
        db_session.commit()
        
        response = client.get("/api/v1/project")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) == 3
    
    def test_update_project_success(
        self, client: TestClient, admin_headers: dict, db_session: Session
    ):
        """Test updating a project."""
        project = Project(
            title="Old Title",
            slug="project-slug",
            short_desc="Old description"
        )
        db_session.add(project)
        db_session.commit()
        db_session.refresh(project)
        
        update_data = {
            "title": "New Title",
            "detailed_desc": "New detailed description",
            "tech_stack": ["React", "Node.js"]
        }
        
        response = client.patch(
            f"/api/v1/project/{project.id}",
            json=update_data,
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["title"] == "New Title"
        assert data["data"]["slug"] == "project-slug"  # Unchanged
        assert len(data["data"]["tech_stack"]) == 2
    
    def test_update_project_slug(
        self, client: TestClient, admin_headers: dict, db_session: Session
    ):
        """Test updating project slug."""
        project = Project(
            title="Test",
            slug="old-slug",
            short_desc="Test"
        )
        db_session.add(project)
        db_session.commit()
        db_session.refresh(project)
        
        response = client.patch(
            f"/api/v1/project/{project.id}",
            json={"slug": "new-slug"},
            headers=admin_headers
        )
        
        assert response.status_code == 200
        assert response.json()["data"]["slug"] == "new-slug"
    
    def test_update_project_not_found(
        self, client: TestClient, admin_headers: dict
    ):
        """Test updating non-existent project."""
        response = client.patch(
            "/api/v1/project/nonexistent-id",
            json={"title": "Updated"},
            headers=admin_headers
        )
        
        assert response.status_code == 404
    
    def test_delete_project_success(
        self, client: TestClient, admin_headers: dict, db_session: Session
    ):
        """Test soft deleting a project."""
        project = Project(
            title="To Delete",
            slug="to-delete",
            short_desc="Will be deleted"
        )
        db_session.add(project)
        db_session.commit()
        db_session.refresh(project)
        
        response = client.delete(
            f"/api/v1/project/{project.id}",
            headers=admin_headers
        )
        
        assert response.status_code == 200
        
        # Verify soft delete
        db_session.refresh(project)
        assert project.is_deleted is True
        
        # Verify not in list
        list_response = client.get("/api/v1/project")
        assert len(list_response.json()["data"]) == 0
    
    def test_upload_cover_image_success(
        self, client: TestClient, admin_headers: dict, db_session: Session
    ):
        """Test uploading a cover image for project."""
        project = Project(
            title="Test",
            slug="test",
            short_desc="Test"
        )
        db_session.add(project)
        db_session.commit()
        db_session.refresh(project)
        
        file_content = b"fake image content"
        files = {
            "file": ("cover.png", BytesIO(file_content), "image/png")
        }
        
        response = client.post(
            f"/api/v1/project/{project.id}/upload-cover",
            files=files,
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "file_path" in data["data"]
    
    def test_upload_project_images(
        self, client: TestClient, admin_headers: dict, db_session: Session
    ):
        """Test uploading multiple project images."""
        project = Project(
            title="Test",
            slug="test",
            short_desc="Test"
        )
        db_session.add(project)
        db_session.commit()
        db_session.refresh(project)
        
        file_content = b"fake image"
        files = {
            "file": ("screenshot.png", BytesIO(file_content), "image/png")
        }
        
        response = client.post(
            f"/api/v1/project/{project.id}/upload-image",
            files=files,
            headers=admin_headers
        )
        
        assert response.status_code == 200
    
    def test_project_with_images_array(
        self, client: TestClient, admin_headers: dict
    ):
        """Test creating project with images array."""
        project_data = {
            "title": "Gallery Project",
            "slug": "gallery-project",
            "short_desc": "Project with images",
            "images": ["/uploads/img1.jpg", "/uploads/img2.jpg"]
        }
        
        response = client.post(
            "/api/v1/project",
            json=project_data,
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]["images"]) == 2
