import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

print("=" * 60)
print("API ENDPOINT TESTS")
print("=" * 60)

# Test 1: Health Check
print("\n1. HEALTH CHECK")
try:
    response = requests.get(f"{BASE_URL}/health")
    print(f"   ✓ Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   ✓ Response: {response.json()}")
except Exception as e:
    print(f"   ✗ ERROR: {e}")

# Test 2: Get Personal Info
print("\n2. GET PERSONAL INFO (Public)")
try:
    response = requests.get(f"{BASE_URL}/personal")
    print(f"   ✓ Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✓ Success: {data.get('success')}")
        print(f"   ✓ Message: {data.get('message')}")
except Exception as e:
    print(f"   ✗ ERROR: {e}")

# Test 3: Login
print("\n3. ADMIN LOGIN")
try:
    login_data = {"email": "admin@example.com", "password": "R@dmin12##"}
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print(f"   ✓ Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"   ✓ Login Success!")
        token = result.get('data', {}).get('access_token')
        
        # Test 4: Get Projects (Public)
        print("\n4. GET PROJECTS (Public)")
        try:
            response = requests.get(f"{BASE_URL}/projects")
            print(f"   ✓ Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   ✓ Success: {data.get('success')}")
                print(f"   ✓ Message: {data.get('message')}")
        except Exception as e:
            print(f"   ✗ ERROR: {e}")
            
        # Test 5: Get Education (Public)
        print("\n5. GET EDUCATION (Public)")
        try:
            response = requests.get(f"{BASE_URL}/education")
            print(f"   ✓ Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   ✓ Success: {data.get('success')}")
                print(f"   ✓ Message: {data.get('message')}")
        except Exception as e:
            print(f"   ✗ ERROR: {e}")
            
        # Test 6: Get Experience (Public)
        print("\n6. GET EXPERIENCE (Public)")
        try:
            response = requests.get(f"{BASE_URL}/experience")
            print(f"   ✓ Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   ✓ Success: {data.get('success')}")
                print(f"   ✓ Message: {data.get('message')}")
        except Exception as e:
            print(f"   ✗ ERROR: {e}")
            
    else:
        print(f"   ✗ Login Failed: {response.status_code}")
        print(f"   ✗ Response: {response.text}")
except Exception as e:
    print(f"   ✗ ERROR: {e}")

print("\n" + "=" * 60)
print("ALL TESTS COMPLETED")
print("=" * 60)
