"""
Model Tests
==========

This module tests the database models directly to ensure:
- Field definitions and types are correct
- Constraints (unique, nullable) are enforced
- Relationships work as expected
- Base model features (UUID, timestamps) function correctly

"""

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.models.user import User, UserRole
from app.models.project import Project
from app.models.base import BaseModel


class TestBaseModelFeatures:
    """
    Tests for shared features inherited from BaseModel.
    """

    def test_uuid_generation(self, db_session: Session):
        """
        Test that ID is automatically generated as ID.
        """
        user = User(
            email="uuid_test@example.com", 
            hashed_password="hash",
            role=UserRole.CONTRIBUTOR
        )
        db_session.add(user)
        db_session.commit()
        
        assert user.id is not None
        assert len(user.id) == 36  # Standard UUID length

    def test_timestamps(self, db_session: Session):
        """
        Test that created_at and updated_at are set automatically.
        """
        user = User(
            email="time_test@example.com", 
            hashed_password="hash"
        )
        db_session.add(user)
        db_session.commit()
        
        assert user.created_at is not None
        assert user.updated_at is not None
        
    def test_soft_delete_default(self, db_session: Session):
        """
        Test that is_deleted defaults to False.
        """
        user = User(
            email="delete_test@example.com", 
            hashed_password="hash"
        )
        db_session.add(user)
        db_session.commit()
        
        assert user.is_deleted is False


class TestUserConstraints:
    """
    Tests for User model constraints.
    """

    def test_email_uniqueness(self, db_session: Session):
        """
        Test that duplicate emails raise IntegrityError.
        """
        user1 = User(email="unique@example.com", hashed_password="hash")
        db_session.add(user1)
        db_session.commit()
        
        user2 = User(email="unique@example.com", hashed_password="hash")
        db_session.add(user2)
        
        with pytest.raises(IntegrityError):
            db_session.commit()
        
        db_session.rollback()


class TestProjectConstraints:
    """
    Tests for Project model constraints.
    """
    
    def test_slug_uniqueness(self, db_session: Session):
        """
        Test that duplicate slugs raise IntegrityError.
        """
        p1 = Project(
            title="P1", 
            slug="unique-slug", 
            short_desc="d1"
        )
        db_session.add(p1)
        db_session.commit()
        
        p2 = Project(
            title="P2", 
            slug="unique-slug", 
            short_desc="d2"
        )
        db_session.add(p2)
        
        with pytest.raises(IntegrityError):
            db_session.commit()
        
        db_session.rollback()
