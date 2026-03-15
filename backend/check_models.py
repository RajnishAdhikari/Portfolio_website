"""
Direct model check - verify what SQLAlchemy sees
"""
import sys
sys.path.insert(0, '.')

from app.models.education import Education
from app.models.experience import Experience
from sqlalchemy import inspect

print("=" * 60)
print("MODEL INSPECTION")
print("=" * 60)

print("\n📋 EDUCATION Model Columns:")
for col in inspect(Education).columns:
    print(f"  - {col.name}: {col.type}")

print("\n📋 EXPERIENCE Model Columns:")
for col in inspect(Experience).columns:
    print(f"  - {col.name}: {col.type}")

print("\n" + "=" * 60)
