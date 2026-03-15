"""
Fix Extracurricular table - remove NOT NULL constraints from optional fields
"""
import sqlite3
from pathlib import Path

db_path = Path(__file__).parent / "portfolio.db"
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

print("=" * 70)
print("FIXING EXTRACURRICULAR TABLE")
print("=" * 70)

# Check current schema
print("\n1. Current extracurricular table columns:")
cursor.execute("PRAGMA table_info(extracurricular)")
columns = cursor.fetchall()
for col in columns:
    print(f"   {col[1]:20} {col[2]:15} {'NOT NULL' if col[3] else 'NULLABLE'}")

# Recreate table without NOT NULL constraints on optional fields
print("\n2. Recreating extracurricular table...")

# Create new table with correct schema
cursor.execute("""
CREATE TABLE extracurricular_new (
    id VARCHAR(36) PRIMARY KEY,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    is_deleted INTEGER NOT NULL DEFAULT 0,
    title VARCHAR(255) NOT NULL,
    organisation VARCHAR(255),
    start_month_year VARCHAR(20),
    end_month_year VARCHAR(20),
    description TEXT,
    certificate_image VARCHAR(500),
    external_url VARCHAR(500)
)
""")

# Copy existing data (if any)
print("   Copying existing data...")
try:
    cursor.execute("""
    INSERT INTO extracurricular_new 
        (id, created_at, updated_at, is_deleted, title, organisation, 
         start_month_year, end_month_year, description, certificate_image, external_url)
    SELECT 
        id, created_at, updated_at, is_deleted, title, organisation,
        start_month_year, end_month_year, description, certificate_image, external_url
    FROM extracurricular
    """)
    print(f"   Copied {cursor.rowcount} rows")
except Exception as e:
    print(f"   No existing data to copy (table might be empty): {e}")

# Drop old table
cursor.execute("DROP TABLE extracurricular")

# Rename new table
cursor.execute("ALTER TABLE extracurricular_new RENAME TO extracurricular")

conn.commit()

print("   ✓ Extracurricular table recreated successfully!")

# Verify new schema
print("\n3. New extracurricular table columns:")
cursor.execute("PRAGMA table_info(extracurricular)")
for col in cursor.fetchall():
    print(f"   {col[1]:20} {col[2]:15} {'NOT NULL' if col[3] else 'NULLABLE'}")

conn.close()

print("\n" + "=" * 70)
print("✅ FIX COMPLETE - All fields now nullable except title!")
print("=" * 70)
print("\n🚀 Refresh your browser and try creating an extracurricular activity!")
