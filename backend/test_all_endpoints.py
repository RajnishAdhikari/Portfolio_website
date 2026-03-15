"""
Test GET endpoints to reproduce the 500 error
"""
import http.client
import json

def test_endpoint(path, name):
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"GET {path}")
    print('='*60)
    
    try:
        conn = http.client.HTTPConnection("localhost", 8000)
        conn.request("GET", path)
        response = conn.getresponse()
        status = response.status
        data = response.read().decode()
        
        print(f"Status: {status}")
        
        if status == 200:
            print("✅ SUCCESS")
            try:
                json_data = json.loads(data)
                print(f"Data items: {len(json_data.get('data', []))}")
            except:
                print(f"Response: {data[:200]}")
        else:
            print(f"❌ FAILED - {status}")
            print(f"Response: {data[:500]}")
        
        conn.close()
        return status == 200
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

print("="*60)
print("TESTING ALL GET ENDPOINTS")
print("="*60)

results = {}
results['Personal'] = test_endpoint("/api/v1/personal", "Personal Info")
results['Education'] = test_endpoint("/api/v1/education", "Education")
results['Experience'] = test_endpoint("/api/v1/experience", "Experience")
results['Skills'] = test_endpoint("/api/v1/skills", "Skills")
results['Projects'] = test_endpoint("/api/v1/projects", "Projects")
results['Articles'] = test_endpoint("/api/v1/articles", "Articles")
results['Certifications'] = test_endpoint("/api/v1/certifications", "Certifications")
results['Extracurricular'] = test_endpoint("/api/v1/extracurricular", "Extracurricular")

print("\n" + "="*60)
print("SUMMARY")
print("="*60)
for name, success in results.items():
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{name:20s} {status}")
print("="*60)
