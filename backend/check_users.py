import sqlite3

conn = sqlite3.connect('portfolio.db')
cursor = conn.cursor()

print("=== USERS IN DATABASE ===")
cursor.execute("SELECT id, email, role FROM users WHERE is_deleted = 0")
users = cursor.fetchall()

for user in users:
    print(f"ID: {user[0]}")
    print(f"Email: {user[1]}")
    print(f"Role: {user[2]}")
    print()

conn.close()
