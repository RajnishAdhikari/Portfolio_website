"""
Complete database and model verification
"""
import sqlite3

DB_PATH = "app.db"

print("=" * 70)
print("DATABASE SCHEMA VERIFICATION")
print("=" * 70)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Check education table
print("\n📋 EDUCATION TABLE:")
cursor.execute("SELECT * FROM education LIMIT 0")
edu_cols = [desc[0] for desc in cursor.description]
print(f"Columns ({len(edu_cols)}):")
for col in edu_cols:
    print(f"  ✓ {col}")

required_edu = ['field', 'location', 'grade']
missing_edu = [col for col in required_edu if col not in edu_cols]
if missing_edu:
    print(f"\n❌ MISSING: {missing_edu}")
else:
    print(f"\n✅ All required columns present!")

# Check experience table
print("\n📋 EXPERIENCE TABLE:")
cursor.execute("SELECT * FROM experience LIMIT 0")
exp_cols = [desc[0] for desc in cursor.description]
print(f"Columns ({len(exp_cols)}):")
for col in exp_cols:
    print(f"  ✓ {col}")

required_exp = ['position', 'location', 'employment_type']
missing_exp = [col for col in required_exp if col not in exp_cols]
if missing_exp:
    print(f"\n❌ MISSING: {missing_exp}")
else:
    print(f"\n✅ All required columns present!")

conn.close()

print("\n" + "=" * 70)
if not missing_edu and not missing_exp:
    print("✅ DATABASE SCHEMA IS CORRECT")
    print("\nIf you're still getting 500 errors:")
    print("1. Stop the server (Ctrl+C)")
    print("2. Restart: python -m uvicorn app.main:app --reload")
else:
    print("❌ DATABASE SCHEMA IS INCOMPLETE")
    print("\nRun these commands:")
    print("1. Stop the server (Ctrl+C)")
    print("2. python create_fresh_db.py")
    print("3. python -m uvicorn app.main:app --reload")
print("=" * 70)
