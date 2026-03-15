"""
Get the FULL error response from the backend
"""
import requests

print("=" * 70)
print("GETTING FULL ERROR RESPONSE FROM EDUCATION ENDPOINT")
print("=" * 70)

# Login first to get token
print("\n1. Logging in...")
login_response = requests.post("http://localhost:8000/api/v1/auth/login", json={
    "email": "admin@example.com",
    "password": "R@dmin12##"
})

if login_response.status_code == 200:
    token = login_response.json().get('data', {}).get('access_token')
    print(f"   ✓ Login successful")
    
    # Test with auth token
    print("\n2. Testing GET /api/v1/education WITH AUTH TOKEN")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get("http://localhost:8000/api/v1/education", headers=headers)
    
    print(f"   Status Code: {response.status_code}")
    print(f"   Response Length: {len(response.text)} bytes")
    
    if response.status_code != 200:
        print("\n   FULL ERROR RESPONSE:")
        print("   " + "=" * 66)
        print(response.text)
        print("   " + "=" * 66)
    else:
        print(f"   ✓ SUCCESS!")
        data = response.json()
        print(f"   Message: {data.get('message')}")
else:
    print(f"   ✗ Login failed: {login_response.status_code}")

print("\n" + "=" * 70)
