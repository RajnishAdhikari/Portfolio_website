import sys
import os
import traceback
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models.user import User
from app.core.security import verify_password

try:
    db = SessionLocal()
    user = db.query(User).filter(User.email == 'admin@example.com').first()
    
    if user:
        print(f"✓ User found: {user.email}")
        print(f"✓ Role: {user.role}")
        print(f"✓ Hash type: {user.hashed_password[:15]}...")
        
        # Test password verification
        is_valid = verify_password("R@dmin12##", user.hashed_password)
        print(f"✓ Password verification: {'SUCCESS' if is_valid else 'FAILED'}")
        
        if not is_valid:
            print("\n❌ PASSWORD DOES NOT MATCH!")
    else:
        print("❌ No user found!")
        
    db.close()
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    traceback.print_exc()
