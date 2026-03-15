import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import sqlite3
import uuid
from datetime import datetime
from app.core.security import get_password_hash

# Connect to database
conn = sqlite3.connect('portfolio.db')
cursor = conn.cursor()

# Delete existing admin if exists
cursor.execute("DELETE FROM users WHERE email = 'admin@example.com'")

# Create new admin user with argon2 hash
user_id = str(uuid.uuid4())
created_at = datetime.utcnow().isoformat()
hashed_password = get_password_hash("R@dmin12##")

cursor.execute("""
    INSERT INTO users (id, email, hashed_password, role, created_at, updated_at, is_deleted)
    VALUES (?, ?, ?, 'admin', ?, ?, 0)
""", (user_id, 'admin@example.com', hashed_password, created_at, created_at))

conn.commit()
conn.close()

print("[SUCCESS] Admin user created with argon2 hash!")
print("  Email: admin@example.com")
print("  Password: R@dmin12##")
print(f"  ID: {user_id}")
