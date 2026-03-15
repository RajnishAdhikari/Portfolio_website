import sqlite3

db_path = 'app.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check current columns
cursor.execute("PRAGMA table_info(education)")
columns = cursor.fetchall()
col_names = [col[1] for col in columns]

print("Current education table columns:")
for col in columns:
    print(f"  {col[1]} ({col[2]})")

# Check if location column exists
if 'location' not in col_names:
    print("\nAdding location column...")
    cursor.execute("ALTER TABLE education ADD COLUMN location VARCHAR(255)")
    conn.commit()
    print("Location column added successfully")
else:
    print("\nLocation column already exists")

conn.close()
