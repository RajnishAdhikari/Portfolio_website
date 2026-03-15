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
    print(f"Token obtained: {token[:30]}...")
    
    # Test 1: Update Personal Info
    print("\n=== TEST 1: Update Personal Info ===")
    personal_data = {
        "full_name": "Test Admin User",
        "email": "admin@example.com",
        "tagline": "Portfolio Admin"
    }
    response = requests.patch(f"{BASE_URL}/personal", json=personal_data, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test 2: Create a Project
    print("\n=== TEST 2: Create Project (Without Cover Image) ===")
    project_data = {
        "title": "Test Project",
        "short_desc": "A test project to verify the fix",
        "tech_stack": ["Python", "FastAPI"]
    }
    response = requests.post(f"{BASE_URL}/projects", json=project_data, headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code in [200, 201]:
        print(f"Response: {json.dumps(response.json(), indent=2)[:500]}...")
    else:
        print(f"Error Response: {response.text}")
    
    # Test 3: Create an Extracurricular Activity
    print("\n=== TEST 3: Create Extracurricular ===")
    extra_data = {
        "title": "Test Activity",
        "organisation": "Test Org",
        "start_month_year": "2024-01"
    }
    response = requests.post(f"{BASE_URL}/extracurricular", json=extra_data, headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code in [200, 201]:
        print(f"Response: {json.dumps(response.json(), indent=2)[:500]}...")
    else:
        print(f"Error Response: {response.text}")
else:
    print(f"Login failed: {login_response.text}")
