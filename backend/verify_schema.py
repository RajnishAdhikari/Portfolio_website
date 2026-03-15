"""
Check the actual database schema to verify migration worked
"""
import sqlite3
from pathlib import Path

backend_dir = Path(__file__).parent
db_path = backend_dir / "portfolio.db"

print("=" * 70)
print("CHECKING DATABASE SCHEMA")
print("=" * 70)
print(f"\nDatabase: {db_path}")
print(f"Exists: {db_path.exists()}")

if not db_path.exists():
    print("ERROR: Database not found!")
    exit(1)

conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# Check education table schema
print("\n📋 EDUCATION TABLE SCHEMA:")
cursor.execute("PRAGMA table_info(education)")
columns = cursor.fetchall()
for col in columns:
    print(f"  {col[1]:20} {col[2]:15} {'NOT NULL' if col[3] else 'NULLABLE'}")

# Check if field column exists
field_exists = any(col[1] == 'field' for col in columns)
print(f"\n✓ 'field' column exists: {field_exists}")

# Check experience table schema  
print("\n📋 EXPERIENCE TABLE SCHEMA:")
cursor.execute("PRAGMA table_info(experience)")
columns = cursor.fetchall()
for col in columns:
    print(f"  {col[1]:20} {col[2]:15} {'NOT NULL' if col[3] else 'NULLABLE'}")

# Check if position column exists
position_exists = any(col[1] == 'position' for col in columns)
print(f"\n✓ 'position' column exists: {position_exists}")

# Now try to query the tables
print("\n🔍 TESTING QUERIES:")

try:
    cursor.execute("SELECT id, institution, degree, field FROM education LIMIT 1")    
    result = cursor.fetchone()
    print(f"✓ Education query: SUCCESS (found {result if result else 'no records'})")
except sqlite3.Error as e:
    print(f"✗ Education query FAILED: {e}")

try:
    cursor.execute("SELECT id, company, position FROM experience LIMIT 1")
    result = cursor.fetchone()
    print(f"✓ Experience query: SUCCESS (found {result if result else 'no records'})")
except sqlite3.Error as e:
    print(f"✗ Experience query FAILED: {e}")

conn.close()
print("\n" + "=" * 70)
