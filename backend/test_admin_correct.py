import urllib.request
import json

# Test admin registration with correct format
print("🧪 Testing Admin Registration (Correct Format)")
print("=" * 50)

admin_data = {
    "username": "admin",
    "email": "admin@example.com", 
    "password": "admin123",
    "full_name": "Admin User",
    "phone": "9999999999",
    "role": "admin"
}

print("1. Testing Admin Registration...")
print("Data:", admin_data)

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
            "email": "admin@example.com",
            "password": "admin123"
        }
        
        login_req = urllib.request.Request("http://localhost:8000/auth/login", data=json.dumps(login_data).encode('utf-8'), headers={'Content-Type': 'application/json'})
        
        with urllib.request.urlopen(login_req) as login_response:
            login_result = login_response.read().decode('utf-8')
            print("✅ Admin Login SUCCESS!")
            print("Login Response:", login_result)
            
            # Check if admin is stored in user_db.csv
            print("\n3. Checking user_db.csv for admin...")
            import pandas as pd
            try:
                df = pd.read_csv("database/user_db.csv")
                print(f"Total users in database: {len(df)}")
                if len(df) > 0:
                    admin_users = df[df['role'] == 'admin']
                    print(f"Admin users: {len(admin_users)}")
                    if len(admin_users) > 0:
                        latest_admin = admin_users.iloc[-1]
                        print(f"Admin Username: {latest_admin['username']}")
                        print(f"Admin Email: {latest_admin['email']}")
                        print(f"Admin Role: {latest_admin['role']}")
                        print(f"Created: {latest_admin['created_at']}")
                        print("\n🎉 Admin data is successfully stored in user_db.csv!")
                    else:
                        print("❌ No admin users found in database")
                else:
                    print("❌ No users found in database")
                
            except Exception as e:
                print(f"Error reading user_db.csv: {e}")
            
except Exception as e:
    print(f"❌ Error: {e}")
    print("\n🔧 Troubleshooting:")
    print("1. Make sure backend is running on http://localhost:8000")
    print("2. Check if the auth endpoints are properly configured")
