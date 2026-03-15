"""
Check if database has correct schema
"""
import sqlite3
import os

DB_PATH = "app.db"

if not os.path.exists(DB_PATH):
    print("❌ DATABASE NOT FOUND!")
    print(f"   {DB_PATH} does not exist")
    print("\nYou need to create it:")
    print("   python create_fresh_db.py")
    exit(1)

print("=" * 70)
print("DATABASE SCHEMA CHECK")
print("=" * 70)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Get education schema
cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='education'")
result = cursor.fetchone()
if result:
    print("\n✅ EDUCATION table exists")
    schema = result[0]
    
    # Check for required columns
    has_field = 'field' in schema.lower()
    has_location = 'location' in schema.lower()
    has_grade = 'grade' in schema.lower()
    
    print(f"   field column: {'✅' if has_field else '❌ MISSING'}")
    print(f"   location column: {'✅' if has_location else '❌ MISSING'}")
    print(f"   grade column: {'✅' if has_grade else '❌ MISSING'}")
    
    edu_ok = has_field and has_location and has_grade
else:
    print("\n❌ EDUCATION table does NOT exist!")
    edu_ok = False

# Get experience schema
cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='experience'")
result = cursor.fetchone()
if result:
    print("\n✅ EXPERIENCE table exists")
    schema = result[0]
    
    # Check for required columns
    has_position = 'position' in schema.lower()
    has_location = 'location' in schema.lower()
    has_employment_type = 'employment_type' in schema.lower()
    
    print(f"   position column: {'✅' if has_position else '❌ MISSING'}")
    print(f"   location column: {'✅' if has_location else '❌ MISSING'}")
    print(f"   employment_type column: {'✅' if has_employment_type else '❌ MISSING'}")
    
    exp_ok = has_position and has_location and has_employment_type
else:
    print("\n❌ EXPERIENCE table does NOT exist!")
    exp_ok = False

conn.close()

print("\n" + "=" * 70)
if edu_ok and exp_ok:
    print("✅ DATABASE SCHEMA IS CORRECT!")
    print("\nIf 500 errors persist:")
    print("1. Make sure server is running: python -m uvicorn app.main:app --reload")
    print("2. Check server terminal for actual error messages")
    exit(0)
else:
    print("❌ DATABASE SCHEMA IS INCOMPLETE OR INCORRECT!")
    print("\n🔧 FIX:")
    print("1. Stop the server if running (Ctrl+C)")
    print("2. Run: python create_fresh_db.py")
    print("3. Start server: python -m uvicorn app.main:app --reload")
    exit(1)

print("=" * 70)
