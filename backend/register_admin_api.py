import requests
import json

# API endpoint
url = 'http://localhost:8000/api/v1/auth/register'

# Admin credentials
data = {
    "email": "admin@example.com",
    "password": "R@dmin12##",
    "role": "admin"
}

# Since register endpoint requires admin auth, we need to create first admin differently
# Let's try without auth and see what happens
try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")
