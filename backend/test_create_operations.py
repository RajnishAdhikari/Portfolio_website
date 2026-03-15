"""
Test Experience GET and Education POST to see specific errors
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

print("=" * 70)
print("TESTING EXPERIENCE & EDUCATION CREATE")
print("=" * 70)

# Login first
print("\n1. Logging in...")
login_response = requests.post(f"{BASE_URL}/auth/login", json={
    "email": "admin@example.com",
    "password": "R@dmin12##"
})

if login_response.status_code != 200:
    print(f"   ✗ Login failed: {login_response.status_code}")
    exit(1)

token = login_response.json().get('data', {}).get('access_token')
headers = {"Authorization": f"Bearer {token}"}
print("   ✓ Login successful")

# Test Experience GET
print("\n2. Testing GET /api/v1/experience")
response = requests.get(f"{BASE_URL}/experience", headers=headers)
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    print("   ✓ SUCCESS!")
else:
    print(f"   ✗ ERROR: {response.text[:500]}")

# Test Education POST
print("\n3. Testing POST /api/v1/education (CREATE)")
edu_data = {
    "institution": "Test University",
    "degree": "Bachelor of Science",
    "field": "Computer Science",
    "start_month_year": "2020-01"
}
response = requests.post(f"{BASE_URL}/education", json=edu_data, headers=headers)
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    print("   ✓ SUCCESS!")
    print(f"   Created: {response.json()}")
else:
    print(f"   ✗ ERROR (first 1000 chars):")
    print(f"   {response.text[:1000]}")

# Test Experience POST
print("\n4. Testing POST /api/v1/experience (CREATE)")
exp_data = {
    "company": "Test Company",
    "position": "Software Engineer",
    "start_month_year": "2021-01"
}
response = requests.post(f"{BASE_URL}/experience", json=exp_data, headers=headers)
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    print("   ✓ SUCCESS!")
    print(f"   Created: {response.json()}")
else:
    print(f"   ✗ ERROR (first 1000 chars):")
    print(f"   {response.text[:1000]}")

print("\n" + "=" * 70)
