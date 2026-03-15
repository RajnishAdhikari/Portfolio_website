import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import AFTER adding to path
from app.core.security import get_password_hash, verify_password

print("Testing password hashing...")
try:
    test_hash = get_password_hash("test123")
    print(f"Hash created: {test_hash[:50]}...")
    print(f"Verification: {verify_password('test123', test_hash)}")
    print("\n✓ Password hashing works!")
    
    # Now create real admin hash
    admin_hash = get_password_hash("R@dmin12##")
    print(f"\nAdmin password hash: {admin_hash}")
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
