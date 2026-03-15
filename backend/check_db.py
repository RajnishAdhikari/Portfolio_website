import sqlite3

conn = sqlite3.connect('portfolio.db')
cursor = conn.cursor()

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

print("=== DATABASE TABLES ===")
for table in tables:
    print(f"- {table[0]}")

# Check users table
print("\n=== USERS TABLE ===")
cursor.execute("SELECT email, role FROM users")
users = cursor.fetchall()
for user in users:
    print(f"Email: {user[0]}, Role: {user[1]}")

# Check personal table
print("\n=== PERSONAL TABLE ===")
cursor.execute("PRAGMA table_info(personal)")
columns = cursor.fetchall()
for col in columns:
    print(f"{col[1]} - Type: {col[2]}, Nullable: {'Yes' if col[3] == 0 else 'No'}")

conn.close()
