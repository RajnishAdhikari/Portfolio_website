"""
Reset Database Script
This script will delete the existing database and create a new one with the updated schema.
IMPORTANT: Stop the uvicorn server before running this script!
"""
import os
import sys
import time

DB_FILE = "app.db"

print("=" * 50)
print("DATABASE RESET SCRIPT")
print("=" * 50)

# Check if database file exists
if os.path.exists(DB_FILE):
    print(f"📁 Found existing database: {DB_FILE}")
    try:
        os.remove(DB_FILE)
        print(f"✅ Deleted old database file")
    except PermissionError:
        print(f"❌ ERROR: Cannot delete {DB_FILE}")
        print(f"   The file is locked (probably by the running server)")
        print(f"\n⚠️  SOLUTION:")
        print(f"   1. Stop the uvicorn server (Ctrl+C in the terminal)")
        print(f"   2. Run this script again: python reset_database.py")
        print(f"   3. Restart the server: python -m uvicorn app.main:app --reload")
        sys.exit(1)
    except Exception as e:
        print(f"❌ ERROR: {e}")
        sys.exit(1)
else:
    print(f"📁 No existing database found")

# Wait a moment for filesystem
time.sleep(0.5)

# Import after deletion to ensure fresh connection
print("\n📦 Importing application modules...")
from app.database import engine, Base, get_db
from app.models.user import User, UserRole
from app.core.security import get_password_hash

# Create all tables with new schema
print("🔨 Creating database tables with new schema...")
Base.metadata.create_all(bind=engine)
print("✅ Tables created successfully")

# Create admin user
print("\n👤 Creating admin user...")
db = next(get_db())
try:
    admin = User(
        email="admin@example.com",
        hashed_password=get_password_hash("R@dmin12##"),
        role=UserRole.ADMIN
    )
    db.add(admin)
    db.commit()
    print("✅ Admin user created successfully!")
    print("\n📋 Login Credentials:")
    print("   Email: admin@example.com")
    print("   Password: R@dmin12##")
except Exception as e:
    print(f"❌ ERROR creating admin: {e}")
    db.rollback()
finally:
    db.close()

print("\n" + "=" * 50)
print("✅ DATABASE RESET COMPLETE!")
print("=" * 50)
print("\n📝 Next steps:")
print("   1. Start the server: python -m uvicorn app.main:app --reload")
print("   2. Try creating Experience/Education entries")
print("=" * 50)
