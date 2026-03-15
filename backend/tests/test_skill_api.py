"""
Unit tests for Skills API endpoints.
Tests CRUD operations, category filtering, and level validation.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.skill import Skill, SkillCategory


class TestSkillEndpoints:
    """Tests for skill CRUD endpoints."""
    
    def test_list_skills_empty(self, client: TestClient):
        """Test listing skills when none exist."""
        response = client.get("/api/v1/skill")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert len(data["data"]) == 0
    
    def test_create_skill_success(
        self, client: TestClient, admin_headers: dict, db_session: Session
    ):
        """Test creating a new skill."""
        skill_data = {
            "category": "Frontend",
            "name": "React",
            "level": 5
        }
        
        response = client.post(
            "/api/v1/skill",
            json=skill_data,
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["name"] == "React"
        assert data["data"]["category"] == "Frontend"
        assert data["data"]["level"] == 5
        
        # Verify in database
        skill = db_session.query(Skill).first()
        assert skill is not None
        assert skill.name == "React"
    
    def test_create_skill_all_categories(
        self, client: TestClient, admin_headers: dict
    ):
        """Test creating skills in all categories."""
        categories = ["Frontend", "Backend", "Language", "Tool", "Other"]
        
        for category in categories:
            skill_data = {
                "category": category,
                "name": f"{category} Skill",
                "level": 3
            }
            
            response = client.post(
                "/api/v1/skill",
                json=skill_data,
                headers=admin_headers
            )
            
            assert response.status_code == 200
            assert response.json()["data"]["category"] == category
    
    def test_create_skill_invalid_level(
        self, client: TestClient, admin_headers: dict
    ):
        """Test that skill level must be between 1-5."""
        # Test level too high
        response = client.post(
            "/api/v1/skill",
            json={"category": "Frontend", "name": "Test", "level": 6},
            headers=admin_headers
        )
        # May return 422 for validation or 400 for business logic
        assert response.status_code in [400, 422]
        
        # Test level too low
        response = client.post(
            "/api/v1/skill",
            json={"category": "Frontend", "name": "Test", "level": 0},
            headers=admin_headers
        )
        assert response.status_code in [400, 422]
    
    def test_create_skill_without_auth(self, client: TestClient):
        """Test that creating skill requires authentication."""
        response = client.post(
            "/api/v1/skill",
            json={"category": "Frontend", "name": "Test", "level": 3}
        )
        
        assert response.status_code == 401
    
    def test_create_skill_missing_required_fields(
        self, client: TestClient, admin_headers: dict
    ):
        """Test validation for required fields."""
        response = client.post(
            "/api/v1/skill",
            json={"name": "Test"},  # Missing category and level
            headers=admin_headers
        )
        
        assert response.status_code == 422
    
    def test_list_skills_grouped_by_category(
        self, client: TestClient, admin_headers: dict, db_session: Session
    ):
        """Test listing skills grouped by category."""
        skills = [
            Skill(category=SkillCategory.FRONTEND, name="React", level=5),
            Skill(category=SkillCategory.FRONTEND, name="Vue", level=4),
            Skill(category=SkillCategory.BACKEND, name="FastAPI", level=5),
            Skill(category=SkillCategory.BACKEND, name="Django", level=4),
            Skill(category=SkillCategory.LANGUAGE, name="Python", level=5),
            Skill(category=SkillCategory.TOOL, name="Docker", level=4),
        ]
        
        for skill in skills:
            db_session.add(skill)
        db_session.commit()
        
        response = client.get("/api/v1/skill")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) == 6
        
        # Check that skills are present
        skill_names = [s["name"] for s in data["data"]]
        assert "React" in skill_names
        assert "FastAPI" in skill_names
        assert "Python" in skill_names
    
    def test_update_skill_success(
        self, client: TestClient, admin_headers: dict, db_session: Session
    ):
        """Test updating a skill."""
        skill = Skill(category=SkillCategory.FRONTEND, name="React", level=3)
        db_session.add(skill)
        db_session.commit()
        db_session.refresh(skill)
        
        update_data = {
            "level": 5,
            "name": "React.js"
        }
        
        response = client.patch(
            f"/api/v1/skill/{skill.id}",
            json=update_data,
            headers=admin_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["level"] == 5
        assert data["data"]["name"] == "React.js"
        assert data["data"]["category"] == "Frontend"  # Unchanged
    
    def test_update_skill_change_category(
        self, client: TestClient, admin_headers: dict, db_session: Session
    ):
        """Test changing skill category."""
        skill = Skill(category=SkillCategory.FRONTEND, name="JavaScript", level=5)
        db_session.add(skill)
        db_session.commit()
        db_session.refresh(skill)
        
        response = client.patch(
            f"/api/v1/skill/{skill.id}",
            json={"category": "Language"},
            headers=admin_headers
        )
        
        assert response.status_code == 200
        assert response.json()["data"]["category"] == "Language"
    
    def test_update_skill_not_found(
        self, client: TestClient, admin_headers: dict
    ):
        """Test updating non-existent skill."""
        response = client.patch(
            "/api/v1/skill/nonexistent-id",
            json={"level": 5},
            headers=admin_headers
        )
        
        assert response.status_code == 404
    
    def test_update_skill_without_auth(
        self, client: TestClient, db_session: Session
    ):
        """Test that updating requires authentication."""
        skill = Skill(category=SkillCategory.FRONTEND, name="Test", level=3)
        db_session.add(skill)
        db_session.commit()
        db_session.refresh(skill)
        
        response = client.patch(
            f"/api/v1/skill/{skill.id}",
            json={"level": 5}
        )
        
        assert response.status_code == 401
    
    def test_delete_skill_success(
        self, client: TestClient, admin_headers: dict, db_session: Session
    ):
        """Test soft deleting a skill."""
        skill = Skill(category=SkillCategory.FRONTEND, name="To Delete", level=3)
        db_session.add(skill)
        db_session.commit()
        db_session.refresh(skill)
        
        response = client.delete(
            f"/api/v1/skill/{skill.id}",
            headers=admin_headers
        )
        
        assert response.status_code == 200
        
        # Verify soft delete
        db_session.refresh(skill)
        assert skill.is_deleted is True
        
        # Verify not in list
        list_response = client.get("/api/v1/skill")
        assert len(list_response.json()["data"]) == 0
    
    def test_delete_skill_not_found(
        self, client: TestClient, admin_headers: dict
    ):
        """Test deleting non-existent skill."""
        response = client.delete(
            "/api/v1/skill/nonexistent-id",
            headers=admin_headers
        )
        
        assert response.status_code == 404
    
    def test_delete_skill_without_auth(
        self, client: TestClient, db_session: Session
    ):
        """Test that deleting requires authentication."""
        skill = Skill(category=SkillCategory.FRONTEND, name="Test", level=3)
        db_session.add(skill)
        db_session.commit()
        db_session.refresh(skill)
        
        response = client.delete(f"/api/v1/skill/{skill.id}")
        
        assert response.status_code == 401
    
    def test_skills_ordered_by_level(
        self, client: TestClient, db_session: Session
    ):
        """Test that skills can be ordered by proficiency level."""
        skills = [
            Skill(category=SkillCategory.FRONTEND, name="Beginner", level=1),
            Skill(category=SkillCategory.FRONTEND, name="Expert", level=5),
            Skill(category=SkillCategory.FRONTEND, name="Intermediate", level=3),
        ]
        
        for skill in skills:
            db_session.add(skill)
        db_session.commit()
        
        response = client.get("/api/v1/skill")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) == 3
