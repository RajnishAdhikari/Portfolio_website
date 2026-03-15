import sqlite3

conn = sqlite3.connect('backend/app.db')
cursor = conn.cursor()

# Get first user
cursor.execute("SELECT id, email FROM users LIMIT 1")
row = cursor.fetchone()

if row:
    print(f"Database ID (raw): '{row[0]}'")
    print(f"Email: '{row[1]}'")
    print(f"ID Length: {len(row[0])}")
    print(f"Has hyphens: {'-' in row[0]}")
else:
    print("No users found")

conn.close()
