import urllib.request
import json

# Test user registration
print("🧪 Testing User Registration and Login System")
print("=" * 50)

# Test registration
register_data = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123",
    "full_name": "Test User",
    "phone": "1234567890",
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
        
        # Test login with the registered user
        print("\n2. Testing User Login...")
        login_data = {
            "email": "test@example.com",
            "password": "password123"
        }
        
        login_req = urllib.request.Request("http://localhost:8000/auth/login", data=json.dumps(login_data).encode('utf-8'), headers={'Content-Type': 'application/json'})
        
        with urllib.request.urlopen(login_req) as login_response:
            login_result = login_response.read().decode('utf-8')
            print("✅ Login SUCCESS!")
            print("Login Response:", login_result)
            
            # Check if user is stored in database
            print("\n3. Checking User Database...")
            import pandas as pd
            try:
                df = pd.read_csv("database/users.csv")
                print(f"Total users in database: {len(df)}")
                print("Latest user:")
                latest_user = df.iloc[-1]
                print(f"Username: {latest_user['username']}")
                print(f"Email: {latest_user['email']}")
                print(f"Role: {latest_user['role']}")
                print(f"Created: {latest_user['created_at']}")
                print("\n🎉 User login data storage is WORKING!")
                
            except Exception as e:
                print(f"Error reading user database: {e}")
                
except Exception as e:
    print(f"❌ Error: {e}")
    print("\n🔧 Troubleshooting:")
    print("1. Make sure backend is running on http://localhost:8000")
    print("2. Check if the auth endpoints are properly configured")
    print("3. Verify the user_service.py is in the services directory")
