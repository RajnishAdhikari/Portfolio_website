import requests

# Test OPTIONS request (preflight)
response = requests.options(
    'http://localhost:8000/api/v1/auth/login',
    headers={
        'Origin': 'http://localhost:5173',
        'Access-Control-Request-Method': 'POST',
        'Access-Control-Request-Headers': 'content-type'
    }
)

print("Status Code:", response.status_code)
print("\nResponse Headers:")
for key, value in response.headers.items():
    if 'access-control' in key.lower() or 'allow' in key.lower():
        print(f"  {key}: {value}")

# Test POST request
post_response = requests.post(
    'http://localhost:8000/api/v1/auth/login',
    headers={
        'Origin': 'http://localhost:5173',
        'Content-Type': 'application/json'
    },
    json={'email': 'admin@example.com', 'password': 'admin123'}
)

print("\n\nPOST Response Status:", post_response.status_code)
print("POST Response Headers:")
for key, value in post_response.headers.items():
    if 'access-control' in key.lower() or 'allow' in key.lower():
        print(f"  {key}: {value}")
