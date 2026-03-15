"""
Standalone database creation script - Windows compatible (no emojis)
"""
import sqlite3
import os

DB_FILE = "app.db"

print("=" * 60)
print("STANDALONE DATABASE CREATION")
print("=" * 60)

# Delete if exists
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)
    print(f"[OK] Deleted old {DB_FILE}")

# Create new database with correct schema
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

print("\n[*] Creating tables...")

# Users table
cursor.execute("""
CREATE TABLE users (
    id TEXT PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL,
    role TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    is_deleted INTEGER NOT NULL DEFAULT 0
)
""")

# Education table with ALL fields
cursor.execute("""
CREATE TABLE education (
    id TEXT PRIMARY KEY,
    institution TEXT NOT NULL,
    degree TEXT NOT NULL,
    field TEXT,
    location TEXT,
    grade TEXT,
    start_month_year TEXT NOT NULL,
    end_month_year TEXT,
    description TEXT,
    logo TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    is_deleted INTEGER NOT NULL DEFAULT 0
)
""")

# Experience table with ALL fields
cursor.execute("""
CREATE TABLE experience (
    id TEXT PRIMARY KEY,
    company TEXT NOT NULL,
    position TEXT NOT NULL,
    location TEXT,
    employment_type TEXT,
    start_month_year TEXT NOT NULL,
    end_month_year TEXT,
    description TEXT,
    logo TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    is_deleted INTEGER NOT NULL DEFAULT 0
)
""")

# Skills table
cursor.execute("""
CREATE TABLE skills (
    id TEXT PRIMARY KEY,
    category TEXT NOT NULL,
    name TEXT NOT NULL,
    level INTEGER NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    is_deleted INTEGER NOT NULL DEFAULT 0
)
""")

# Personal table
cursor.execute("""
CREATE TABLE personal (
    id TEXT PRIMARY KEY,
    full_name TEXT NOT NULL,
    tagline TEXT,
    email TEXT NOT NULL,
    phone TEXT,
    address TEXT,
    github_url TEXT,
    linkedin_url TEXT,
    twitter_url TEXT,
    profile_pic TEXT,
    cv_file TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    is_deleted INTEGER NOT NULL DEFAULT 0
)
""")

# Media assets table
cursor.execute("""
CREATE TABLE media_assets (
    id TEXT PRIMARY KEY,
    file_name TEXT NOT NULL,
    file_path TEXT NOT NULL,
    file_type TEXT NOT NULL,
    file_size INTEGER NOT NULL,
    width INTEGER,
    height INTEGER,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    is_deleted INTEGER NOT NULL DEFAULT 0
)
""")

# Projects table
cursor.execute("""
CREATE TABLE projects (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    slug TEXT UNIQUE NOT NULL,
    short_desc TEXT NOT NULL,
    detailed_desc TEXT,
    cover_image TEXT,
    images TEXT,
    pdf_attachment TEXT,
    external_url TEXT,
    github_url TEXT,
    tech_stack TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    is_deleted INTEGER NOT NULL DEFAULT 0
)
""")

# Articles table
cursor.execute("""
CREATE TABLE articles (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    slug TEXT UNIQUE NOT NULL,
    excerpt TEXT NOT NULL,
    body TEXT,
    cover_image TEXT,
    pdf_attachment TEXT,
    external_url TEXT,
    is_featured INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    is_deleted INTEGER NOT NULL DEFAULT 0
)
""")

# Resource papers table
cursor.execute("""
CREATE TABLE resource_papers (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    slug TEXT UNIQUE NOT NULL,
    excerpt TEXT NOT NULL,
    body TEXT,
    cover_image TEXT,
    pdf_attachment TEXT,
    external_url TEXT,
    is_featured INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    is_deleted INTEGER NOT NULL DEFAULT 0
)
""")

# Certifications table
cursor.execute("""
CREATE TABLE certifications (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    issuer TEXT NOT NULL,
    issue_month_year TEXT NOT NULL,
    cred_id TEXT,
    cred_url TEXT,
    description TEXT,
    image TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    is_deleted INTEGER NOT NULL DEFAULT 0
)
""")

# Extracurricular table
cursor.execute("""
CREATE TABLE extracurricular (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    organisation TEXT NOT NULL,
    start_month_year TEXT NOT NULL,
    end_month_year TEXT,
    description TEXT,
    certificate_image TEXT,
    external_url TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    is_deleted INTEGER NOT NULL DEFAULT 0
)
""")

# Refresh tokens table
cursor.execute("""
CREATE TABLE refresh_tokens (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    refresh_token_hash TEXT UNIQUE NOT NULL,
    expires_at TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    is_deleted INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users (id)
)
""")

conn.commit()
print("[OK] All tables created successfully!")

# Create admin user
from datetime import datetime
import uuid

try:
    from app.core.security import get_password_hash
    
    admin_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()
    
    cursor.execute("""
        INSERT INTO users (id, email, hashed_password, role, created_at, updated_at, is_deleted)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (admin_id, "admin@example.com", get_password_hash("R@dmin12##"), "admin", now, now, 0))
    
    conn.commit()
    print("\n[OK] Admin user created!")
    print("   Email: admin@example.com")
    print("   Password: R@dmin12##")
except Exception as e:
    print(f"\n[WARNING] Could not create admin user: {e}")
    print("   You can create it manually after starting the server")

conn.close()

print("\n" + "=" * 60)
print("[SUCCESS] DATABASE CREATED SUCCESSFULLY!")
print("=" * 60)
print("\nNow start the server:")
print("  python -m uvicorn app.main:app --reload")
print("=" * 60)
