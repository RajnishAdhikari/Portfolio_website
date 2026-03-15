import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

# Login first to get auth token
print("=" * 70)
print("TESTING EDUCATION, EXPERIENCE, AND SKILLS ENDPOINTS")
print("=" * 70)

print("\n1. LOGIN TO GET AUTH TOKEN")
login_response = requests.post(f"{BASE_URL}/auth/login", json={
    "email": "admin@example.com",
    "password": "R@dmin12##"
})

if login_response.status_code != 200:
    print(f"   ✗ Login failed: {login_response.status_code}")
    print(f"   Response: {login_response.text}")
    exit(1)

token = login_response.json().get('data', {}).get('access_token')
headers = {"Authorization": f"Bearer {token}"}
print(f"   ✓ Login successful! Token obtained.")

# Test Education
print("\n2. TEST EDUCATION ENDPOINT (GET)")
try:
    response = requests.get(f"{BASE_URL}/education")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✓ Success: {data.get('message')}")
    else:
        print(f"   ✗ ERROR: {response.text}")
except Exception as e:
    print(f"   ✗ Exception: {e}")

# Test Experience
print("\n3. TEST EXPERIENCE ENDPOINT (GET)")
try:
    response = requests.get(f"{BASE_URL}/experience")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✓ Success: {data.get('message')}")
    else:
        print(f"   ✗ ERROR: {response.text}")
except Exception as e:
    print(f"   ✗ Exception: {e}")

# Test Skills GET
print("\n4. TEST SKILLS ENDPOINT (GET)")
try:
    response = requests.get(f"{BASE_URL}/skills")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✓ Success: {data.get('message')}")
    else:
        print(f"   ✗ ERROR: {response.text}")
except Exception as e:
    print(f"   ✗ Exception: {e}")

# Test Skills CREATE
print("\n5. TEST SKILLS CREATE (POST)")
try:
    skill_data = {
        "category": "frontend",
        "name": "React",
        "level": 4
    }
    response = requests.post(f"{BASE_URL}/skills", json=skill_data, headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✓ Success: {data.get('message')}")
    else:
        print(f"   ✗ ERROR Response:")
        print(f"   {response.text}")
except Exception as e:
    print(f"   ✗ Exception: {e}")

print("\n" + "=" * 70)
print("TESTS COMPLETED")
print("=" * 70)
