import urllib.request
import json

# Test user registration
print("🧪 Testing User Registration in user_db.csv")
print("=" * 50)

register_data = {
    "username": "newuser",
    "email": "newuser@example.com",
    "password": "password123",
    "full_name": "New User",
    "phone": "9876543210",
    "role": "user"
}

print("1. Testing User Registration...")
print("Data:", register_data)

try:
    data = json.dumps(register_data).encode('utf-8')
    req = urllib.request.Request("http://localhost:8000/auth/register", data=data, headers={'Content-Type': 'application/json'})
    
    with urllib.request.urlopen(req) as response:
        result = response.read().decode('utf-8')
        print("✅ Registration SUCCESS!")
        print("Response:", result)
        
        # Check if user is stored in user_db.csv
        print("\n2. Checking user_db.csv...")
        import pandas as pd
        try:
            df = pd.read_csv("database/user_db.csv")
            print(f"Total users in database: {len(df)}")
            print("Latest user:")
            latest_user = df.iloc[-1]
            print(f"Username: {latest_user['username']}")
            print(f"Email: {latest_user['email']}")
            print(f"Role: {latest_user['role']}")
            print(f"Created: {latest_user['created_at']}")
            print("\n🎉 User data is now stored in user_db.csv!")
            
        except Exception as e:
            print(f"Error reading user_db.csv: {e}")
            
except Exception as e:
    print(f"❌ Error: {e}")
    print("\n🔧 Troubleshooting:")
    print("1. Make sure backend is running on http://localhost:8000")
    print("2. Check if the auth endpoints are properly configured")
