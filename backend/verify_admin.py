import sqlite3
from passlib.context import CryptContext

# Check current admin user
conn = sqlite3.connect('portfolio.db')
cursor = conn.cursor()

cursor.execute("SELECT email, hashed_password, role FROM users WHERE email = 'admin@example.com'")
result = cursor.fetchone()

if result:
    print(f"Admin user found:")
    print(f"  Email: {result[0]}")
    print(f"  Role: {result[2]}")
    print(f"  Hash (first 50 chars): {result[1][:50]}...")
    
    # Test password verification
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    try:
        is_valid = pwd_context.verify("R@dmin12##", result[1])
        print(f"\nPassword verification test: {'SUCCESS' if is_valid else 'FAILED'}")
    except Exception as e:
        print(f"\nPassword verification ERROR: {e}")
else:
    print("No admin user found!")

conn.close()
