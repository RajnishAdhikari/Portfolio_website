import requests
import json

url = 'http://localhost:8000/api/v1/auth/login'
data = {
    'email': 'admin@example.com',
    'password': 'R@dmin12##'
}

try:
    print("Sending login request...")
    response = requests.post(url, json=data)
    
    print(f"\nStatus Code: {response.status_code}")
    print(f"\nHeaders:")
    for key, value in response.headers.items():
        print(f"  {key}: {value}")
    
    print(f"\nResponse Body:")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
