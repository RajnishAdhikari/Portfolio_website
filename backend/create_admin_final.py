import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import sqlite3
import uuid
from datetime import datetime
from app.core.security import get_password_hash
from app.models.user import UserRole

# Connect to database
conn = sqlite3.connect('portfolio.db')
cursor = conn.cursor()

# Create new admin user with argon2 hash and CORRECT role
user_id = str(uuid.uuid4())
created_at = datetime.utcnow().isoformat()
hashed_password = get_password_hash("R@dmin12##")

# Use the Enum VALUE directly - UserRole.ADMIN.value gives "admin"
cursor.execute("""
    INSERT INTO users (id, email, hashed_password, role, created_at, updated_at, is_deleted)
    VALUES (?, ?, ?, ?, ?, ?, 0)
""", (user_id, 'admin@example.com', hashed_password, UserRole.ADMIN.value, created_at, created_at))

conn.commit()

# Verify
cursor.execute("SELECT email, role FROM users WHERE email = 'admin@example.com'")
result = cursor.fetchone()
conn.close()

print("[SUCCESS] Admin user created!")
print(f"  Email: {result[0]}")
print(f"  Role in DB: '{result[1]}'")
print(f"  Expected: '{UserRole.ADMIN.value}'")
print(f"  Match: {result[1] == UserRole.ADMIN.value}")
