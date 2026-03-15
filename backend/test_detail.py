import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

# Login first
print("=== LOGGING IN ===")
login_response = requests.post(
    f"{BASE_URL}/auth/login",
    json={"email": "admin@example.com", "password": "R@dmin12##"}
)
print(f"Login Status: {login_response.status_code}")

if login_response.status_code == 200:
    token = login_response.json()['data']['access_token']
    headers = {"Authorization": f"Bearer {token}"}
    print(f"Token obtained")
    
    # Test 1: Update Personal Info
    print("\n=== TEST: Update Personal Info ===")
    personal_data = {
        "full_name": "Test Admin User",
        "email": "admin@example.com",
        "tagline": "Portfolio Admin"
    }
    try:
        response = requests.patch(f"{BASE_URL}/personal", json=personal_data, headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        print(f"Raw Content: {response.text[:1000]}")
        
        if response.headers.get('content-type', '').startswith('application/json'):
            print(f"JSON Response: {json.dumps(response.json(), indent=2)}")
        else:
            print("NOT JSON RESPONSE!")
            print(f"Content-Type: {response.headers.get('content-type')}")
    except Exception as e:
        print(f"EXCEPTION: {type(e).__name__}: {e}")
        print(f"Response text: {response.text[:1000]}")
else:
    print(f"Login failed: {login_response.text}")
