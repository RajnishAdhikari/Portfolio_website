"""
Fix Experience table - remove old 'role' column that conflicts with 'position'
"""
import sqlite3
from pathlib import Path

db_path = Path(__file__).parent / "portfolio.db"
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

print("=" * 70)
print("FIXING EXPERIENCE TABLE")
print("=" * 70)

# Check current schema
print("\n1. Current experience table columns:")
cursor.execute("PRAGMA table_info(experience)")
columns = cursor.fetchall()
for col in columns:
    print(f"   {col[1]:20} {col[2]:15} {'NOT NULL' if col[3] else 'NULLABLE'}")

# SQLite doesn't support DROP COLUMN directly, so we need to:
# 1. Create a new table without 'role'
# 2. Copy data from old table
# 3. Drop old table
# 4. Rename new table

print("\n2. Recreating experience table without 'role' column...")

# Create new table with correct schema (matching the model)
cursor.execute("""
CREATE TABLE experience_new (
    id VARCHAR(36) PRIMARY KEY,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    is_deleted INTEGER NOT NULL DEFAULT 0,
    company VARCHAR(255) NOT NULL,
    position VARCHAR(255) NOT NULL,
    location VARCHAR(255),
    employment_type VARCHAR(100),
    start_month_year VARCHAR(20) NOT NULL,
    end_month_year VARCHAR(20),
    description TEXT,
    logo VARCHAR(500)
)
""")

# Copy existing data (if any)
print("   Copying existing data...")
cursor.execute("""
INSERT INTO experience_new 
    (id, created_at, updated_at, is_deleted, company, position, location, 
     employment_type, start_month_year, end_month_year, description, logo)
SELECT 
    id, created_at, updated_at, is_deleted, company, position, location,
    employment_type, start_month_year, end_month_year, description, logo
FROM experience
""")

# Drop old table
cursor.execute("DROP TABLE experience")

# Rename new table
cursor.execute("ALTER TABLE experience_new RENAME TO experience")

conn.commit()

print("   ✓ Experience table recreated successfully!")

# Verify new schema
print("\n3. New experience table columns:")
cursor.execute("PRAGMA table_info(experience)")
for col in cursor.fetchall():
    print(f"   {col[1]:20} {col[2]:15} {'NOT NULL' if col[3] else 'NULLABLE'}")

conn.close()

print("\n" + "=" * 70)
print("✅ FIX COMPLETE - Experience table now matches the model!")
print("=" * 70)
print("\n🚀 Now refresh your browser and try creating an experience entry!")
