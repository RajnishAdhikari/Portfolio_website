"""
Fix refresh_tokens table schema
"""
import sqlite3
import os

DB_FILE = "app.db"

print("=" * 60)
print("FIXING REFRESH_TOKENS TABLE")
print("=" * 60)

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

try:
    # Check current schema
    cursor.execute("PRAGMA table_info(refresh_tokens)")
    cols = cursor.fetchall()
    print("\n📋 Current columns:")
    for col in cols:
        print(f"  - {col[1]}")
    
    # Drop and recreate table  
    print("\n🔨 Recreating table with correct schema...")
    cursor.execute("DROP TABLE IF EXISTS refresh_tokens")
    
    cursor.execute("""
    CREATE TABLE refresh_tokens (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        refresh_token_hash TEXT UNIQUE NOT NULL,
        expires_at TEXT NOT NULL,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        is_deleted INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)
    
    cursor.execute("CREATE INDEX ix_refresh_tokens_user_id ON refresh_tokens (user_id)")
    
    print("\n✅ Table recreated successfully!")
    
    # Verify new schema
    cursor.execute("PRAGMA table_info(refresh_tokens)")
    cols = cursor.fetchall()
    print("\n📋 New columns:")
    for col in cols:
        print(f"  - {col[1]}")
    
    conn.commit()
    print("\n" + "=" * 60)
    print("✅ REFRESH_TOKENS TABLE FIXED!")
    print("=" * 60)
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    conn.rollback()
finally:
    conn.close()
