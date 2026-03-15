"""
Database validation script to verify schema correctness.
Checks all tables, columns, relationships, and constraints.
"""
import sys
from sqlalchemy import inspect
from sqlalchemy.exc import OperationalError

from app.database import engine, Base
from app.models.user import User
from app.models.personal import Personal
from app.models.education import Education
from app.models.experience import Experience
from app.models.skill import Skill
from app.models.project import Project
from app.models.article import Article
from app.models.certification import Certification
from app.models.extracurricular import Extracurricular
from app.models.resource_paper import ResourcePaper
from app.models.refresh_token import RefreshToken


def validate_database():
    """Validate database schema matches models."""
    print("=" * 80)
    print("DATABASE VALIDATION")
    print("=" * 80)
    
    # Create inspector
    inspector = inspect(engine)
    
    # Expected tables
    expected_tables = {
        'users',
        'personal',
        'education',
        'experience',
        'skills',
        'projects',
        'articles',
        'certifications',
        'extracurricular',
        'resource_papers',
        'refresh_tokens'
    }
    
    # Get actual tables
    actual_tables = set(inspector.get_table_names())
    
    print(f"\n✓ Database Engine: {engine.url}")
    print(f"\n1. TABLE VALIDATION")
    print("-" * 80)
    
    # Check all expected tables exist
    missing_tables = expected_tables - actual_tables
    extra_tables = actual_tables - expected_tables
    
    if missing_tables:
        print(f"✗ Missing tables: {', '.join(missing_tables)}")
        return False
    else:
        print(f"✓ All {len(expected_tables)} expected tables exist")
    
    if extra_tables:
        print(f"⚠ Extra tables found: {', '.join(extra_tables)}")
    
    print(f"\nTables in database:")
    for table in sorted(actual_tables):
        columns = inspector.get_columns(table)
        print(f"  - {table}: {len(columns)} columns")
    
    # Validate base model columns exist in all tables
    print(f"\n2. BASE MODEL VALIDATION")
    print("-" * 80)
    
    base_columns = ['id', 'created_at', 'updated_at', 'is_deleted']
    
    for table in expected_tables:
        columns = {col['name'] for col in inspector.get_columns(table)}
        missing_base_cols = set(base_columns) - columns
        
        if missing_base_cols:
            print(f"✗ Table '{table}' missing base columns: {missing_base_cols}")
            return False
    
    print(f"✓ All tables have base model columns: {', '.join(base_columns)}")
    
    # Validate specific model fields
    print(f"\n3. MODEL-SPECIFIC VALIDATION")
    print("-" * 80)
    
    validations = [
        ('users', ['email', 'hashed_password', 'role']),
        ('personal', ['full_name', 'email', 'profile_pic', 'cv_file']),
        ('education', ['institution', 'degree', 'start_month_year', 'logo']),
        ('experience', ['company', 'position', 'start_month_year', 'logo']),
        ('skills', ['category', 'name', 'level']),
        ('projects', ['title', 'slug', 'short_desc', 'tech_stack']),
        ('articles', ['title', 'slug', 'excerpt', 'is_featured']),
        ('certifications', ['name', 'issuer', 'issue_month_year']),
        ('extracurricular', ['title', 'organisation', 'certificate_image']),
        ('resource_papers', ['title', 'slug', 'excerpt', 'is_featured']),
        ('refresh_tokens', ['user_id', 'refresh_token_hash', 'expires_at']),
    ]
    
    all_valid = True
    for table, required_cols in validations:
        columns = {col['name'] for col in inspector.get_columns(table)}
        missing = set(required_cols) - columns
        
        if missing:
            print(f"✗ Table '{table}' missing columns: {missing}")
            all_valid = False
        else:
            print(f"✓ Table '{table}' has all required columns")
    
    if not all_valid:
        return False
    
    # Validate indexes
    print(f"\n4. INDEX VALIDATION")
    print("-" * 80)
    
    indexes_to_check = [
        ('users', 'email'),
        ('projects', 'slug'),
        ('articles', 'slug'),
        ('resource_papers', 'slug'),
    ]
    
    for table, column in indexes_to_check:
        indexes = inspector.get_indexes(table)
        index_columns = [idx['column_names'] for idx in indexes]
        
        # Check if column is indexed (may be in unique constraint too)
        is_indexed = any(column in cols for cols in index_columns)
        
        if is_indexed:
            print(f"✓ Index found for {table}.{column}")
        else:
            # Check unique constraints
            unique_constraints = inspector.get_unique_constraints(table)
            is_unique = any(column in constraint['column_names'] for constraint in unique_constraints)
            if is_unique:
                print(f"✓ Unique constraint found for {table}.{column}")
            else:
                print(f"⚠ No index or unique constraint for {table}.{column}")
    
    # Validate foreign keys
    print(f"\n5. FOREIGN KEY VALIDATION")
    print("-" * 80)
    
    fk_tables = ['refresh_tokens']
    
    for table in fk_tables:
        foreign_keys = inspector.get_foreign_keys(table)
        
        if foreign_keys:
            print(f"✓ Table '{table}' has {len(foreign_keys)} foreign key(s)")
            for fk in foreign_keys:
                print(f"  - {fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}")
        else:
            print(f"⚠ Table '{table}' has no foreign keys")
    
    # Test soft delete
    print(f"\n6. SOFT DELETE VALIDATION")
    print("-" * 80)
    
    for table in expected_tables:
        columns = {col['name']: col for col in inspector.get_columns(table)}
        
        if 'is_deleted' in columns:
            is_deleted_col = columns['is_deleted']
            # Check default value
            if is_deleted_col.get('default') or is_deleted_col.get('nullable') == False:
                print(f"✓ Table '{table}' has is_deleted with proper constraints")
            else:
                print(f"⚠ Table '{table}' is_deleted may not have default value")
        else:
            print(f"✗ Table '{table}' missing is_deleted column")
            return False
    
    print("\n" + "=" * 80)
    print("✓ DATABASE VALIDATION COMPLETE - ALL CHECKS PASSED")
    print("=" * 80)
    return True


if __name__ == "__main__":
    try:
        # Try to create all tables first
        print("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("✓ Tables created successfully\n")
        
        # Validate
        success = validate_database()
        
        if success:
            sys.exit(0)
        else:
            print("\n✗ Validation failed")
            sys.exit(1)
            
    except OperationalError as e:
        print(f"\n✗ Database connection error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
