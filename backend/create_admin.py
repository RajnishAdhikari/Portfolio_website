"""
Initialize admin user for the portfolio application
Run this script after database reset to create the default admin user
"""
from app.database import engine, Base, get_db
from app.models.user import User, UserRole
from app.core.security import get_password_hash

# Create tables
Base.metadata.create_all(bind=engine)

# Create admin user
db = next(get_db())
try:
    # Check if admin already exists
    existing_admin = db.query(User).filter(User.email == "admin@example.com").first()
    
    if existing_admin:
        print("⚠️  Admin user already exists")
    else:
        admin = User(
            email="admin@example.com",
            hashed_password=get_password_hash("R@dmin12##"),
            role=UserRole.ADMIN
        )
        db.add(admin)
        db.commit()
        print("✅ Admin user created successfully")
        print("   Email: admin@example.com")
        print("   Password: R@dmin12##")
finally:
    db.close()
