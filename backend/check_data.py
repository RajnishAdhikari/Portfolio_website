from app.database import SessionLocal
from app.models.personal import Personal
from app.models.education import Education
from app.models.experience import Experience
from app.models.skill import Skill

db = SessionLocal()

# Check Personal Info
personal = db.query(Personal).filter(Personal.is_deleted == False).first()
print(f"Personal Info: {personal}")
if personal:
    print(f"  Name: {personal.full_name}")
    print(f"  Email: {personal.email}")
    print(f"  Is_deleted: {personal.is_deleted}")

# Check Education
education_count = db.query(Education).filter(Education.is_deleted == False).count()
print(f"\nEducation records (not deleted): {education_count}")

# Check Experience
experience_count = db.query(Experience).filter(Experience.is_deleted == False).count()
print(f"Experience records (not deleted): {experience_count}")

# Check Skills
skills_count = db.query(Skill).filter(Skill.is_deleted == False).count()
print(f"Skills records (not deleted): {skills_count}")

db.close()
