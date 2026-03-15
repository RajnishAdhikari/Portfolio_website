import sqlite3db = sqlite3.connect("portfolio.db")
cur = db.cursor()

print("Experience table schema:")
cur.execute("PRAGMA table_info(experience)")
for row in cur.fetchall():
    print(f"  {row[1]}: {row[2]}")

print("\nEducation table schema:")
cur.execute("PRAGMA table_info(education)")  
for row in cur.fetchall():
    print(f"  {row[1]}: {row[2]}")
    
db.close()
