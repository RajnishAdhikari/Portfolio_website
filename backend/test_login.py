"""
Test login endpoint with admin credentials
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_login():
    print("=" * 60)
    print("TESTING LOGIN ENDPOINT")
    print("=" * 60)
    
    # Test credentials
    credentials = {
        "email": "admin@example.com",
        "password": "R@dmin12##"
    }
    
    print(f"\n📝 Attempting login with:")
    print(f"   Email: {credentials['email']}")
    print(f"   Password: {credentials['password']}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/auth/login",
            json=credentials,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"\n📡 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ LOGIN SUCCESSFUL!")
            print(f"\n📋 Response Data:")
            print(f"   Success: {data.get('success')}")
            print(f"   Message: {data.get('message')}")
            if data.get('data'):
                print(f"   Access Token: {data['data'].get('access_token', 'N/A')[:50]}...")
                print(f"   Token Type: {data['data'].get('token_type', 'N/A')}")
            
            # Test authenticated endpoint
            if data.get('data', {}).get('access_token'):
                print("\n🔒 Testing authenticated endpoint...")
                token = data['data']['access_token']
                headers = {"Authorization": f"Bearer {token}"}
                
                test_response = requests.get(
                    f"{BASE_URL}/api/v1/personal",
                    headers=headers
                )
                print(f"   Personal Info Endpoint: {test_response.status_code}")
                if test_response.status_code == 200:
                    print("   ✅ Authentication working!")
                else:
                    print(f"   ❌ Auth failed: {test_response.text[:200]}")
                    
        else:
            print(f"❌ LOGIN FAILED!")
            print(f"\n📋 Error Response:")
            try:
                error_data = response.json()
                print(f"   {json.dumps(error_data, indent=2)}")
            except:
                print(f"   {response.text[:500]}")
                
    except requests.exceptions.ConnectionError:
        print("❌ CANNOT CONNECT TO SERVER!")
        print("   Make sure the server is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ ERROR: {e}")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    test_login()
