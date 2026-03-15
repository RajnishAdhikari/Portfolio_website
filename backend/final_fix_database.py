"""
FINAL DATABASE FIX
This will delete the old database and create a fresh one with ALL correct columns
"""
import os
import subprocess
import sys

print("=" * 70)
print("FINAL DATABASE FIX")
print("=" * 70)

DB_FILE = "app.db"

# Step 1: Delete old database
print("\n1️⃣  Deleting old database...")
if os.path.exists(DB_FILE):
    try:
        os.remove(DB_FILE)
        print(f"   ✅ Deleted {DB_FILE}")
    except PermissionError:
        print(f"   ❌ Cannot delete - file is locked!")
        print(f"   SOLUTION: Stop the server first (Ctrl+C), then run this script again")
        exit(1)
else:
    print(f"   ℹ️  No database file found")

# Step 2: Create fresh database
print("\n2️⃣  Creating fresh database with correct schema...")
result = subprocess.run([sys.executable, "create_fresh_db.py"], 
                       capture_output=True, text=True)

if result.returncode == 0:
    print("   ✅ Database created successfully!")
    print(result.stdout[-300:] if len(result.stdout) > 300 else result.stdout)
else:
    print("   ❌ Error creating database:")
    print(result.stderr)
    exit(1)

# Step 3: Verify schema
print("\n3️⃣  Verifying database schema...")
import sqlite3
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Check education
cursor.execute("SELECT * FROM education LIMIT 0")
edu_cols = [d[0] for d in cursor.description]
has_edu_fields = all(col in edu_cols for col in ['field', 'location', 'grade'])

# Check experience  
cursor.execute("SELECT * FROM experience LIMIT 0")
exp_cols = [d[0] for d in cursor.description]
has_exp_fields = all(col in exp_cols for col in ['position', 'location', 'employment_type'])

conn.close()

if has_edu_fields and has_exp_fields:
    print("   ✅ Education table: field, location, grade ✓")
    print("   ✅ Experience table: position, location, employment_type ✓")
else:
    print("   ❌ Schema verification failed!")
    if not has_edu_fields:
        print(f"   Education missing: {[c for c in ['field', 'location', 'grade'] if c not in edu_cols]}")
    if not has_exp_fields:
        print(f"   Experience missing: {[c for c in ['position', 'location', 'employment_type'] if c not in exp_cols]}")
    exit(1)

print("\n" + "=" * 70)
print("✅ DATABASE IS READY!")
print("=" * 70)
print("\nNow start the server:")
print("   python -m uvicorn app.main:app --reload")
print("\nLogin credentials:")
print("   Email: admin@example.com")
print("   Password: R@dmin12##")
print("=" * 70)
