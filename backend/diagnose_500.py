"""
Comprehensive endpoint test with detailed error output
"""
import http.client
import json
import sys

def test_endpoint_detailed(path, name):
    print(f"\n{'='*70}")
    print(f"Testing: {name}")
    print(f"Endpoint: GET {path}")
    print('='*70)
    
    try:
        conn = http.client.HTTPConnection("localhost", 8000, timeout=5)
        conn.request("GET", path)
        response = conn.getresponse()
        status = response.status
        data = response.read().decode('utf-8')
        
        print(f"Status Code: {status}")
        
        if status == 200:
            print("✅ SUCCESS")
            try:
                json_data = json.loads(data)
                if isinstance(json_data.get('data'), list):
                    print(f"Items returned: {len(json_data['data'])}")
                print(f"Success: {json_data.get('success')}")
                print(f"Message: {json_data.get('message')}")
            except Exception as e:
                print(f"Response preview: {data[:300]}")
        elif status == 500:
            print("❌ 500 INTERNAL SERVER ERROR")
            print("\nError Response:")
            print(data[:1000])  # Show more of the error
            
            # Try to extract error from JSON
            try:
                error_data = json.loads(data)
                if 'detail' in error_data:
                    print(f"\nError Detail: {error_data['detail']}")
            except:
                pass
        else:
            print(f"❌ ERROR - Status {status}")
            print(f"Response: {data[:500]}")
        
        conn.close()
        return status
        
    except ConnectionRefusedError:
        print("❌ Cannot connect to server!")
        print("   Make sure server is running on http://localhost:8000")
        return None
    except Exception as e:
        print(f"❌ Exception: {e}")
        import traceback
        traceback.print_exc()
        return None

print("="*70)
print("ENDPOINT DIAGNOSTIC TEST")
print("="*70)

# Test each endpoint
endpoints = [
    ("/api/v1/personal", "Personal Info"),
    ("/api/v1/education", "Education"),
    ("/api/v1/experience", "Experience"),
    ("/api/v1/skills", "Skills"),
]

results = {}
for path, name in endpoints:
    status = test_endpoint_detailed(path, name)
    results[name] = status
    if status == 500:
        print(f"\n🔍 Found 500 error in {name}! Check the server terminal for stack trace.")
        break  # Stop at first 500 to focus on it

print("\n" + "="*70)
print("SUMMARY")
print("="*70)
for name, status in results.items():
    if status == 200:
        print(f"{name:20s} ✅ OK")
    elif status == 500:
        print(f"{name:20s} ❌ 500 ERROR")
    elif status is None:
        print(f"{name:20s} ⚠️  CONNECTION ERROR")
    else:
        print(f"{name:20s} ❌ {status}")
print("="*70)
