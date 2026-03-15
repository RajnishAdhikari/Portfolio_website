"""
Simple test - call the backend directly to get the error
"""
import requests

url = "http://localhost:8000/api/v1/education"
print(f"Testing: {url}")

try:
    response = requests.get(url)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 500:
        print("\nERROR RESPONSE (first 2000 chars):")
        print(response.text[:2000])
        print("\n...")
    else:
        print(f"Success! Data: {response.json()}")
except Exception as e:
    print(f"Exception: {e}")
