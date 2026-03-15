"""
Simple login test without external dependencies
"""
import http.client
import json

def test_login():
    print("=" * 60)
    print("LOGIN TEST")
    print("=" * 60)
    
    try:
        # Create connection
        conn = http.client.HTTPConnection("localhost", 8000)
        
        # Prepare request
        headers = {'Content-Type': 'application/json'}
        body = json.dumps({
            "email": "admin@example.com",
            "password": "R@dmin12##"
        })
        
        print("\n📝 Sending login request...")
        print(f"   Email: admin@example.com")
        print(f"   Password: R@dmin12##")
        
        # Send request
        conn.request("POST", "/api/v1/auth/login", body, headers)
        
        # Get response
        response = conn.getresponse()
        status = response.status
        data = response.read().decode()
        
        print(f"\n📡 Response Status: {status}")
        
        if status == 200:
            print("✅ LOGIN SUCCESSFUL!")
            response_data = json.loads(data)
            print(f"\n📋 Response:")
            print(f"   Success: {response_data.get('success')}")
            print(f"   Message: {response_data.get('message')}")
            if response_data.get('data', {}).get('access_token'):
                token = response_data['data']['access_token']
                print(f"   Access Token: {token[:50]}...")
                print(f"\n✅ Authentication is WORKING!")
            return True
        else:
            print(f"❌ LOGIN FAILED - Status {status}")
            print(f"\n📋 Response:")
            print(data)
            return False
            
    except ConnectionRefusedError:
        print("❌ SERVER NOT RUNNING!")
        print("   Please start: python -m uvicorn app.main:app --reload")
        return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False
    finally:
        conn.close()
    
    print("=" * 60)

if __name__ == "__main__":
    success = test_login()
    exit(0 if success else 1)
