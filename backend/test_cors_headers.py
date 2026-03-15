# Quick test to verify CORS headers are being sent
import requests

try:
    # Test OPTIONS preflight
    response = requests.options(
        'http://localhost:8000/api/v1/auth/login',
        headers={
            'Origin': 'http://localhost:5173',
            'Access-Control-Request-Method': 'POST',
            'Access-Control-Request-Headers': 'content-type'
        }
    )
    
    print("OPTIONS Response:")
    print(f"Status: {response.status_code}")
    print("\nCORS Headers:")
    for key, value in response.headers.items():
        if 'access-control' in key.lower() or 'allow' in key.lower():
            print(f"  {key}: {value}")
    
    if not any('access-control-allow-origin' in k.lower() for k in response.headers.keys()):
        print("\n❌ NO Access-Control-Allow-Origin header found!")
    else:
        print("\n✓ CORS headers present")
        
except Exception as e:
    print(f"Error: {e}")
