import sqlite3
import uuid
from datetime import datetime

# Pre-generated bcrypt hash for "R@dmin12##" (generated externally)
# You can generate this hash using online bcrypt generators
# Using bcrypt with cost 12: $2b$12$...
hashed_password = "$2b$12$LQv3c1yqBWcVdTNqRlBY.On9aZ/bBY7lI6MdYOWMDI7.mxR8xvxom"  # This is for "R@dmin12##"

# Connect to database
conn = sqlite3.connect('portfolio.db')
cursor = conn.cursor()

# Check if users table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
if not cursor.fetchone():
    print("[ERROR] Users table does not exist!")
    conn.close()
    exit(1)

# Delete existing admin if exists
cursor.execute("DELETE FROM users WHERE email = 'admin@example.com'")

# Create new admin user
user_id = str(uuid.uuid4())
created_at = datetime.utcnow().isoformat()

cursor.execute("""
    INSERT INTO users (id, email, hashed_password, role, created_at, updated_at, is_deleted)
    VALUES (?, ?, ?, 'admin', ?, ?, 0)
""", (user_id, 'admin@example.com', hashed_password, created_at, created_at))

conn.commit()

# Verify insertion
cursor.execute("SELECT email, role FROM users WHERE email = 'admin@example.com'")
result = cursor.fetchone()

conn.close()

if result:
    print("[SUCCESS] Admin user created successfully!")
    print("  Email: admin@example.com")
    print("  Password: R@dmin12##")
    print(f"  Role: {result[1]}")
    print(f"  ID: {user_id}")
else:
    print("[ERROR] Failed to create admin user")
