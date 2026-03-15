import requests

# Test1: Experience GET
print("1. Experience GET:")
r = requests.get("http://localhost:8000/api/v1/experience")
print(f"   {r.status_code} - {'OK' if r.status_code == 200 else 'FAIL'}")

# Test 2: Education POST with minimal data
print("2. Education POST:")
token_r = requests.post("http://localhost:8000/api/v1/auth/login", json={"email": "admin@example.com", "password": "R@dmin12##"})
token = token_r.json()['data']['access_token']
r = requests.post("http://localhost:8000/api/v1/education", 
                  json={"institution": "Test", "degree": "BS", "start_month_year": "2020-01"},
                  headers={"Authorization": f"Bearer {token}"})
print(f"   {r.status_code} - {'OK' if r.status_code == 200 else r.text[:200]}")

# Test 3: Experience POST with minimal data  
print("3. Experience POST:")
r = requests.post("http://localhost:8000/api/v1/experience",
                  json={"company": "Test Co", "position": "Dev", "start_month_year": "2021-01"},
                  headers={"Authorization": f"Bearer {token}"})
print(f"   {r.status_code} - {'OK' if r.status_code == 200 else r.text[:200]}")
