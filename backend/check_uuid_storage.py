import sqlite3
from uuid import UUID

conn = sqlite3.connect('portfolio.db')
cursor = conn.cursor()

print("=== CHECKING UUID STORAGE ===")

# Get the user
cursor.execute("SELECT id, email FROM users WHERE is_deleted = 0 LIMIT 1")
result = cursor.fetchone()

if result:
    stored_id = result[0]
    email = result[1]
    
    print(f"Stored ID type: {type(stored_id)}")
    print(f"Stored ID value: {stored_id}")
    print(f"Stored ID repr: {repr(stored_id)}")
    print(f"Email: {email}")
    
    # Try to convert to UUID
    try:
        if isinstance(stored_id, str):
            uuid_obj = UUID(stored_id)
            print(f"\nConverted to UUID: {uuid_obj}")
            print(f"UUID type: {type(uuid_obj)}")
        elif isinstance(stored_id, bytes):
            print(f"\nStored as bytes, length: {len(stored_id)}")
            # Try to convert from bytes
            try:
                uuid_obj = UUID(bytes=stored_id)
                print(f"Converted from bytes: {uuid_obj}")
            except:
                uuid_obj = UUID(stored_id.decode())
                print(f"Converted from decoded string: {uuid_obj}")
    except Exception as e:
        print(f"\nError converting: {e}")

# Check table schema
print("\n=== TABLE SCHEMA ===")
cursor.execute("PRAGMA table_info(users)")
columns = cursor.fetchall()
for col in columns:
    if col[1] == 'id':
        print(f"ID column: {col}")

conn.close()
