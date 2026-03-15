"""
Direct test of Education endpoint to see actual error
"""
import requests
import json

print("=" * 70)
print("TESTING EDUCATION ENDPOINT DIRECTLY")
print("=" * 70)

# Test without auth first
print("\n1. Testing GET /api/v1/education (no auth)")
try:
    response = requests.get("http://localhost:8000/api/v1/education")
    print(f"   Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"   ✓ SUCCESS!")
        data = response.json()
        print(f"   Message: {data.get('message')}")
    else:
        print(f"   ✗ ERROR Response:")
        print(f"   {response.text[:500]}")
except Exception as e:
    print(f"   ✗ Exception: {e}")

# Test experience endpoint
print("\n2. Testing GET /api/v1/experience (no auth)")
try:
    response = requests.get("http://localhost:8000/api/v1/experience")
    print(f"   Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"   ✓ SUCCESS!")
        data = response.json()
        print(f"   Message: {data.get('message')}")
    else:
        print(f"   ✗ ERROR Response:")
        print(f"   {response.text[:500]}")
except Exception as e:
    print(f"   ✗ Exception: {e}")

# Test skills endpoint
print("\n3. Testing GET /api/v1/skills (no auth)")
try:
    response = requests.get("http://localhost:8000/api/v1/skills")
    print(f"   Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"   ✓ SUCCESS!")
        data = response.json()
        print(f"   Message: {data.get('message')}")
    else:
        print(f"   ✗ ERROR Response:")
        print(f"   {response.text[:500]}")
except Exception as e:
    print(f"   ✗ Exception: {e}")

print("\n" + "=" * 70)
