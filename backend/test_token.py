import requests
import json

# Test with the actual token from the user's browser
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyMGRmNGE5Mi02YmM4LTQ5YzQtOGI3ZC1mNWRhZjkyMDg3ZGEiLCJleHAiOjE3NjQ2OTcyODQsInR5cGUiOiJhY2Nlc3MifQ.JUM-lz-ETWB1boxsoBR1D4iP32YRQBV-2AhCH6vxfv8"

headers = {
    "Authorization": f"Bearer {token}"
}

# Test the personal endpoint
response = requests.patch(
    "http://localhost:8000/api/v1/personal",
    json={"full_name": "Test User", "email": "test@example.com"},
    headers=headers
)

print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")
