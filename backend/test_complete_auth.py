import urllib.request
import json

print("🧪 Testing Complete Authentication System")
print("=" * 50)

# Test admin registration
print("1. Testing Admin Registration...")
admin_data = {
    "username": "admin2",
    "email": "admin2@example.com", 
    "password": "admin123",
    "full_name": "Admin User 2",
    "phone": "8888888888",
    "role": "admin"
}

try:
    data = json.dumps(admin_data).encode('utf-8')
    req = urllib.request.Request("http://localhost:8000/auth/register", data=data, headers={'Content-Type': 'application/json'})
    
    with urllib.request.urlopen(req) as response:
        result = response.read().decode('utf-8')
        print("✅ Admin Registration SUCCESS!")
        print("Response:", result)
        
        # Test admin login
        print("\n2. Testing Admin Login...")
        login_data = {
            "email": "admin2@example.com",
            "password": "admin123"
        }
        
        login_req = urllib.request.Request("http://localhost:8000/auth/login", data=json.dumps(login_data).encode('utf-8'), headers={'Content-Type': 'application/json'})
        
        with urllib.request.urlopen(login_req) as login_response:
            login_result = login_response.read().decode('utf-8')
            print("✅ Admin Login SUCCESS!")
            print("Login Response:", login_result)
            
            # Check final database state
            print("\n3. Final Database Check...")
            import pandas as pd
            df = pd.read_csv("database/user_db.csv")
            print(f"Total users in database: {len(df)}")
            print("Users:")
            for _, user in df.iterrows():
                print(f"  - {user['username']} ({user['role']}) - {user['email']}")
            
            print("\n🎉 User authentication system is working!")
            print("✅ Registration: Working")
            print("✅ Login: Working") 
            print("✅ Data Storage: Working")
            print("✅ Database: user_db.csv")
            
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
