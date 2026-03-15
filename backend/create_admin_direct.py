import sqlite3
import uuid
from datetime import datetime
from passlib.context import CryptContext

# Initialize password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash the password
password = "R@dmin12##"
hashed = pwd_context.hash(password)

# Connect to database
conn = sqlite3.connect('portfolio.db')
cursor = conn.cursor()

# Delete existing admin if exists
cursor.execute("DELETE FROM users WHERE email = 'admin@example.com'")

# Create new admin user
user_id = str(uuid.uuid4())
created_at = datetime.utcnow().isoformat()

cursor.execute("""
    INSERT INTO users (id, email, hashed_password, role, created_at, updated_at, is_deleted)
    VALUES (?, ?, ?, 'admin', ?, ?, 0)
""", (user_id, 'admin@example.com', hashed, created_at, created_at))

conn.commit()
conn.close()

print("[SUCCESS] Admin user created successfully!")
print("  Email: admin@example.com")
print("  Password: R@dmin12##")
print(f"  ID: {user_id}")
