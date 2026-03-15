"""
Database Schema Migration Script
Adds missing columns to education and experience tables
"""
import sqlite3
import os
from pathlib import Path

# Get database path - use portfolio.db as specified in .env
backend_dir = Path(__file__).parent
db_path = backend_dir / "portfolio.db"

print("=" * 70)
print("DATABASE SCHEMA MIGRATION")
print("=" * 70)

if not db_path.exists():
    print(f"\n❌ ERROR: Database not found at {db_path}")
    print("Please ensure the database exists before running migration.")
    exit(1)

print(f"\n📁 Database: {db_path}")
print(f"📊 Size: {os.path.getsize(db_path)} bytes")

# Connect to database
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

try:
    # Check if education table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='education'")
    if not cursor.fetchone():
        print("\n⚠️  WARNING: education table does not exist. Creating it...")
        # Table will be created by SQLAlchemy on next server start
    else:
        # Check if 'field' column exists
        cursor.execute("PRAGMA table_info(education)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'field' in columns:
            print("\n✓ education.field column already exists")
        else:
            print("\n➕ Adding 'field' column to education table...")
            cursor.execute("ALTER TABLE education ADD COLUMN field VARCHAR(255)")
            print("✓ Successfully added education.field column")
    
    # Check if experience table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='experience'")
    if not cursor.fetchone():
        print("\n⚠️  WARNING: experience table does not exist. Creating it...")
        # Table will be created by SQLAlchemy on next server start
    else:
        # Check if 'position' column exists
        cursor.execute("PRAGMA table_info(experience)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'position' in columns:
            print("\n✓ experience.position column already exists")
        else:
            print("\n➕ Adding 'position' column to experience table...")
            cursor.execute("ALTER TABLE experience ADD COLUMN position VARCHAR(255)")
            print("✓ Successfully added experience.position column")
    
    # Commit changes
    conn.commit()
    
    print("\n" + "=" * 70)
    print("✅ MIGRATION COMPLETED SUCCESSFULLY")
    print("=" * 70)
    
    # Display updated schema
    print("\n📋 Updated Schema:")
    print("\nEducation Table:")
    cursor.execute("PRAGMA table_info(education)")
    for col in cursor.fetchall():
        print(f"  - {col[1]} ({col[2]})")
    
    print("\nExperience Table:")
    cursor.execute("PRAGMA table_info(experience)")
    for col in cursor.fetchall():
        print(f"  - {col[1]} ({col[2]})")

except sqlite3.Error as e:
    print(f"\n❌ ERROR during migration: {e}")
    conn.rollback()
    exit(1)

finally:
    conn.close()

print("\n✅ Database connection closed")
print("🚀 You can now restart the backend server")
