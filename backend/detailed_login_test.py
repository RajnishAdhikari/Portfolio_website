"""
Detailed login test with full error output
"""
import sys
import traceback
sys.path.insert(0, '.')

from app.database import get_db
from app.models.user import User
from app.core.security import verify_password, create_access_token, create_refresh_token
from datetime import datetime, timedelta
from app.models.refresh_token import RefreshToken
from app.config import get_settings

settings = get_settings()

print("=" * 60)
print("DETAILED LOGIN TEST")
print("=" * 60)

db = next(get_db())

try:
    # Find user
    print("\n1️⃣ Finding user...")
    user = db.query(User).filter(
        User.email == "admin@example.com",
        User.is_deleted == False
    ).first()
    
    if not user:
        print("❌ User not found!")
        exit(1)
    
    print(f"✅ User found: {user.email} (ID: {user.id[:8]}...)")
    
    # Verify password
    print("\n2️⃣ Verifying password...")
    if not verify_password("R@dmin12##", user.hashed_password):
        print("❌ Password incorrect!")
        exit(1)
    
    print("✅ Password correct!")
    
    # Create tokens
    print("\n3️⃣ Creating access token...")
    access_token = create_access_token(data={"sub": str(user.id)})
    print(f"✅ Access token created: {access_token[:50]}...")
    
    print("\n4️⃣ Creating refresh token...")
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    print(f"✅ Refresh token created: {refresh_token[:50]}...")
    
    # Store refresh token
    print("\n5️⃣ Storing refresh token in database...")
    print(f"   user_id: {user.id} (type: {type(user.id).__name__})")
    print(f"   refresh_token_hash: {refresh_token[:30]}...")
    print(f"   expires_at: {datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)}")
    
    refresh_token_obj = RefreshToken(
        user_id=user.id,
        refresh_token_hash=refresh_token,
        expires_at=datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)
    )
    
    print(f"   RefreshToken object created")
    print(f"   Attributes: {refresh_token_obj.__dict__}")
    
    db.add(refresh_token_obj)
    print("   Added to session")
    
    db.commit()
    print("✅ Stored in database!")
    
    print("\n" + "=" * 60)
    print("✅ LOGIN TEST SUCCESSFUL!")
    print("=" * 60)
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    print(f"\nFull traceback:")
    traceback.print_exc()
    db.rollback()
finally:
    db.close()
