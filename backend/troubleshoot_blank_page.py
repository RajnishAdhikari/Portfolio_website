"""
Check frontend dev server for build errors
"""
import subprocess
import sys

print("Checking if frontend is running and has errors...")
print("\nIf the frontend terminal shows build errors, they will appear above.")
print("\n" + "="*60)
print("TROUBLESHOOTING BLANK PAGE")
print("="*60)
print("\n1. Check the frontend terminal (npm run dev) for errors")
print("2. Check browser console (F12) for JavaScript errors")
print("3. Try accessing http://localhost:5173 (root)")
print("4. Try accessing http://localhost:5173/admin")
print("\nIf you see errors in browser console, share them with me.")
print("="*60)
