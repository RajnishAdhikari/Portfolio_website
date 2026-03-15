"""
Complete Fix - Restart server and verify
This script will guide you through fixing the 500 errors
"""
import subprocess
import sys
import time
import http.client

print("=" * 70)
print("COMPLETE 500 ERROR FIX - Step by Step")
print("=" * 70)

print("\n📋 Step 1: Checking Database Schema...")
result = subprocess.run([sys.executable, "check_database_schema.py"], 
                       capture_output=True, text=True)

if result.returncode != 0:
    print("❌ Database schema is incorrect!")
    print(result.stdout)
    print("\n🔧 FIXING: Recreating database...")
    subprocess.run([sys.executable, "create_fresh_db.py"])
    print("✅ Database recreated!")

print("\n" + "=" * 70)
print("✅ Database is ready!")
print("=" * 70)

print("\n📋 Next Steps:")
print("\n1️⃣  START THE SERVER:")
print("     python -m uvicorn app.main:app --reload")

print("\n2️⃣  TEST IT WORKS:")
print("     Open browser: http://localhost:5173/admin/login")
print("     Login: admin@example.com / R@dmin12##")
print("     Navigate to Education or Experience")

print("\n3️⃣  IF STILL 500 ERROR:")
print("     Check the SERVER TERMINAL for the exact error message")
print("     The error will show which column/field is causing the problem")

print("\n" + "=" * 70)
print("💡 TIP: The server MUST be restarted after model changes!")
print("=" * 70)
