"""
Database Migration Script - Add Missing Columns
This adds the missing columns to existing tables without losing data.
Can be run while the server is running.
"""
import sqlite3

DB_PATH = "app.db"

print("=" * 60)
print("DATABASE MIGRATION - Adding Missing Columns")
print("=" * 60)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

try:
    print("\n📋 Migrating EXPERIENCE table...")
    
    # Check current columns
    cursor.execute("PRAGMA table_info(experience)")
    columns = {row[1] for row in cursor.fetchall()}
    print(f"   Current columns: {columns}")
    
    # Add new columns if they don't exist
    if 'position' not in columns:
        print("   Adding 'position' column...")
        cursor.execute("ALTER TABLE experience ADD COLUMN position TEXT")
        # Copy data from role to position
        cursor.execute("UPDATE experience SET position = role WHERE position IS NULL")
        print("   ✅ Added position (copied from role)")
    
    if 'location' not in columns:
        print("   Adding 'location' column...")
        cursor.execute("ALTER TABLE experience ADD COLUMN location TEXT")
        print("   ✅ Added location")
    
    if 'employment_type' not in columns:
        print("   Adding 'employment_type' column...")
        cursor.execute("ALTER TABLE experience ADD COLUMN employment_type TEXT")
        print("   ✅ Added employment_type")
    
    print("\n📋 Migrating EDUCATION table...")
    
    # Check current columns
    cursor.execute("PRAGMA table_info(education)")
    columns = {row[1] for row in cursor.fetchall()}
    print(f"   Current columns: {columns}")
    
    # Add new columns if they don't exist
    if 'field' not in columns:
        print("   Adding 'field' column...")
        cursor.execute("ALTER TABLE education ADD COLUMN field TEXT")
        print("   ✅ Added field")
    
    if 'location' not in columns:
        print("   Adding 'location' column...")
        cursor.execute("ALTER TABLE education ADD COLUMN location TEXT")
        print("   ✅ Added location")
    
    if 'grade' not in columns:
        print("   Adding 'grade' column...")
        cursor.execute("ALTER TABLE education ADD COLUMN grade TEXT")
        print("   ✅ Added grade")
    
    conn.commit()
    print("\n" + "=" * 60)
    print("✅ MIGRATION COMPLETE!")
    print("=" * 60)
    print("\n📝 The server will auto-reload and pick up the changes.")
    print("   You can now create Experience and Education entries!")
    print("=" * 60)
    
except Exception as e:
    conn.rollback()
    print(f"\n❌ ERROR: {e}")
    print("\nIf you see 'database is locked', try:")
    print("1. Stop the server (Ctrl+C)")
    print("2. Run this script again")
    print("3. Restart the server")
finally:
    conn.close()
