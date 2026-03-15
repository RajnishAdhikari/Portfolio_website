import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

print("=== TESTING API ENDPOINTS ===\n")

# Test 1: Health check
print("1. Health Check")
try:
    response = requests.get(f"{BASE_URL}/health")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}\n")
except Exception as e:
    print(f"   ERROR: {e}\n")

# Test 2: Get personal info
print("2. Get Personal Info (Public)")
try:
    response = requests.get(f"{BASE_URL}/personal")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}\n")
except Exception as e:
    print(f"   ERROR: {e}\n")

# Test 3: Login
print("3. Login with admin credentials")
try:
    login_data = {
        "email": "admin@example.com",
        "password": "R@dmin12##"
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"   Success: Login successful")
        token = result.get('data', {}).get('access_token')
        print(f"   Token: {token[:50]}..." if token else "   Token: None")
        
        # Test 4: Update Personal Info (requires auth)
        if token:
            print("\n4. Update Personal Info (Authenticated)")
            headers = {"Authorization": f"Bearer {token}"}
            update_data = {
                "full_name": "Test Admin",
                "email": "admin@example.com"
            }
            try:
                response = requests.patch(f"{BASE_URL}/personal", json=update_data, headers=headers)
                print(f"   Status: {response.status_code}")
                if response.status_code == 200:
                    print(f"   Response: {response.json()}")
                else:
                    print(f"   ERROR Response: {response.text}")
            except Exception as e:
                print(f"   ERROR: {e}")
    else:
        print(f"   ERROR Response: {response.text}")
except Exception as e:
    print(f"   ERROR: {e}\n")
