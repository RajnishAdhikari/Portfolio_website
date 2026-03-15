#!/usr/bin/env python
"""
Interactive terminal script to test Personal Info API
"""
import requests
import json
from getpass import getpass

BASE_URL = "http://localhost:8000/api/v1"

def login():
    """Login and get access token"""
    print("\n=== LOGIN ===")
    email = input("Email (default: admin@example.com): ").strip() or "admin@example.com"
    password = getpass("Password (default: R@dmin12##): ") or "R@dmin12##"
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json={"email": email, "password": password}
        )
        
        if response.status_code == 200:
            data = response.json()
            token = data['data']['access_token']
            print(f"✅ Login successful!")
            return token
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def get_personal_info(token):
    """Get current personal info"""
    print("\n=== GETTING CURRENT PERSONAL INFO ===")
    try:
        response = requests.get(
            f"{BASE_URL}/personal",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        print(f"Status: {response.status_code}")
        data = response.json()
        print(json.dumps(data, indent=2))
        return data.get('data')
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def update_personal_info(token):
    """Update personal info"""
    print("\n=== UPDATE PERSONAL INFO ===")
    print("Enter new values (press Enter to skip):")
    
    full_name = input("Full Name: ").strip()
    tagline = input("Tagline: ").strip()
    email = input("Email: ").strip()
    phone = input("Phone: ").strip()
    address = input("Address: ").strip()
    linkedin = input("LinkedIn URL: ").strip()
    github = input("GitHub URL: ").strip()
    twitter = input("Twitter URL: ").strip()
    
    # Build update payload
    update_data = {}
    if full_name: update_data['full_name'] = full_name
    if tagline: update_data['tagline'] = tagline
    if email: update_data['email'] = email
    if phone: update_data['phone'] = phone
    if address: update_data['address'] = address
    if linkedin: update_data['linkedin_url'] = linkedin
    if github: update_data['github_url'] = github
    if twitter: update_data['twitter_url'] = twitter
    
    if not update_data:
        print("⚠️ No data to update!")
        return
    
    print(f"\nSending data: {json.dumps(update_data, indent=2)}")
    
    try:
        response = requests.patch(
            f"{BASE_URL}/personal",
            json=update_data,
            headers={"Authorization": f"Bearer {token}"}
        )
        
        print(f"\n📡 Response Status: {response.status_code}")
        print(f"📄 Response:")
        
        try:
            print(json.dumps(response.json(), indent=2))
        except:
            print(response.text)
            
        if response.status_code == 200:
            print("\n✅ Personal info updated successfully!")
        else:
            print(f"\n❌ Update failed with status {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    print("=" * 60)
    print("  PERSONAL INFO API TESTER")
    print("=" * 60)
    
    # Login
    token = login()
    if not token:
        print("\n❌ Cannot proceed without valid token")
        return
    
    while True:
        print("\n" + "=" * 60)
        print("  MENU")
        print("=" * 60)
        print("1. Get current personal info")
        print("2. Update personal info")
        print("3. Login again")
        print("4. Exit")
        
        choice = input("\nChoice: ").strip()
        
        if choice == "1":
            get_personal_info(token)
        elif choice == "2":
            update_personal_info(token)
        elif choice == "3":
            token = login()
            if not token:
                print("❌ Login failed")
        elif choice == "4":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    main()
