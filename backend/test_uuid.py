from app.database import engine
from sqlalchemy import text

with engine.connect() as conn:
    # Get first user
    result = conn.execute(text("SELECT id, email FROM users LIMIT 1"))
    row = result.fetchone()
    if row:
        print(f"Database ID (raw): '{row[0]}'")
        print(f"Email: '{row[1]}'")
        print(f"ID Length: {len(row[0])}")
        print(f"Has hyphens: {'-' in row[0]}")
    else:
        print("No users found")
