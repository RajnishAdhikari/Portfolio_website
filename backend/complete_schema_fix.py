"""
Complete database schema fix - add ALL missing columns
"""
import sqlite3
from pathlib import Path

backend_dir = Path(__file__).parent
db_path = backend_dir / "portfolio.db"

print("=" * 70)
print("COMPLETE DATABASE SCHEMA FIX")
print("=" * 70)

conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

try:
    # Get current education table columns  
    cursor.execute("PRAGMA table_info(education)")
    edu_columns = {col[1] for col in cursor.fetchall()}
    print(f"\n📋 Current education columns: {edu_columns}")
    
    # Required education columns from the model
    required_edu = {
        'id', 'created_at', 'updated_at', 'is_deleted',  # BaseModel fields
        'institution', 'degree', 'field', 'location', 'grade',  # Education fields
        'start_month_year', 'end_month_year', 'description', 'logo'
    }
    
    missing_edu = required_edu - edu_columns
    print(f"❌ Missing education columns: {missing_edu}")
    
    # Add missing education columns
    for col in missing_edu:
        if col in ['id', 'created_at', 'updated_at', 'is_deleted']:
            continue  # Skip BaseModel fields
        
        col_type = {
            'institution': 'VARCHAR(255)',
            'degree': 'VARCHAR(255)',
            'field': 'VARCHAR(255)',
            'location': 'VARCHAR(255)',
            'grade': 'VARCHAR(50)',
            'start_month_year': 'VARCHAR(20)',
            'end_month_year': 'VARCHAR(20)',
            'description': 'TEXT',
            'logo': 'VARCHAR(500)'
        }.get(col, 'TEXT')
        
        print(f"  ➕ Adding education.{col} ({col_type})")
        cursor.execute(f"ALTER TABLE education ADD COLUMN {col} {col_type}")
    
    # Get current experience table columns
    cursor.execute("PRAGMA table_info(experience)")
    exp_columns = {col[1] for col in cursor.fetchall()}
    print(f"\n📋 Current experience columns: {exp_columns}")
    
    # Required experience columns from the model
    required_exp = {
        'id', 'created_at', 'updated_at', 'is_deleted',  # BaseModel fields
        'company', 'position', 'location', 'employment_type',  # Experience fields
        'start_month_year', 'end_month_year', 'description', 'logo'
    }
    
    missing_exp = required_exp - exp_columns
    print(f"❌ Missing experience columns: {missing_exp}")
    
    # Add missing experience columns
    for col in missing_exp:
        if col in ['id', 'created_at', 'updated_at', 'is_deleted']:
            continue  # Skip BaseModel fields
        
        col_type = {
            'company': 'VARCHAR(255)',
            'position': 'VARCHAR(255)',
            'location': 'VARCHAR(255)',
            'employment_type': 'VARCHAR(100)',
            'start_month_year': 'VARCHAR(20)',
            'end_month_year': 'VARCHAR(20)',
            'description': 'TEXT',
            'logo': 'VARCHAR(500)'
        }.get(col, 'TEXT')
        
        print(f"  ➕ Adding experience.{col} ({col_type})")
        cursor.execute(f"ALTER TABLE experience ADD COLUMN {col} {col_type}")
    
    conn.commit()
    
    print("\n" + "=" * 70)
    print("✅ ALL MISSING COLUMNS ADDED SUCCESSFULLY!")
    print("=" * 70)
    
    # Verify
    print("\n📋 Final education schema:")
    cursor.execute("PRAGMA table_info(education)")
    for col in cursor.fetchall():
        if col[1] not in ['id', 'created_at', 'updated_at', 'is_deleted']:
            print(f"  ✓ {col[1]}")
    
    print("\n📋 Final experience schema:")
    cursor.execute("PRAGMA table_info(experience)")
    for col in cursor.fetchall():
        if col[1] not in ['id', 'created_at', 'updated_at', 'is_deleted']:
            print(f"  ✓ {col[1]}")

except sqlite3.Error as e:
    print(f"\n❌ ERROR: {e}")
    conn.rollback()
finally:
    conn.close()

print("\n🚀 RESTART the backend server now!")
