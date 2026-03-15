"""
Check actual database schema
"""
import sqlite3

DB_PATH = "app.db"

print("=" * 60)
print("CHECKING DATABASE SCHEMA")
print("=" * 60)

try:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("\n📋 EDUCATION table columns:")
    cursor.execute("PRAGMA table_info(education)")
    columns = cursor.fetchall()
    for col in columns:
        print(f"   - {col[1]} ({col[2]})")
    
    print("\n📋 EXPERIENCE table columns:")
    cursor.execute("PRAGMA table_info(experience)")
    columns = cursor.fetchall()
    for col in columns:
        print(f"   - {col[1]} ({col[2]})")
    
    conn.close()
    print("\n" + "=" * 60)
    
except Exception as e:
    print(f"ERROR: {e}")
