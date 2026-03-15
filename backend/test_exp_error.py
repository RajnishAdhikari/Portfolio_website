import requests

print("Testing Experience POST with full error:")
token_r = requests.post("http://localhost:8000/api/v1/auth/login", json={"email": "admin@example.com", "password": "R@dmin12##"})
token = token_r.json()['data']['access_token']

r = requests.post("http://localhost:8000/api/v1/experience",
                  json={"company": "Test Co", "position": "Dev", "start_month_year": "2021-01"},
                  headers={"Authorization": f"Bearer {token}"})

print(f"Status: {r.status_code}")
if r.status_code != 200:
    # Print full error
    print("\nFull error response:")
    print(r.text)
