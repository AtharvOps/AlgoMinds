import urllib.request
import json

# Test the exact data structure that the frontend sends
frontend_claim_data = {
    "claim_amount": 25000.0,
    "repair_estimate": 15000.0,
    "previous_claims": 1,
    "policy_validity": 24,
    "image_uploaded": 0,
    "damage_consistency": 1,
    "user_phone": "9876543210",
    "garage_id": "GAR002",
    "agent_id": "AG002",
    "garage_city": "Delhi",
    "accident_location": "Delhi"
}

print("Testing claim submission with frontend data structure...")
print("Data being sent:", frontend_claim_data)

try:
    data = json.dumps(frontend_claim_data).encode('utf-8')
    req = urllib.request.Request("http://localhost:8000/predict", data=data, headers={'Content-Type': 'application/json'})
    
    with urllib.request.urlopen(req) as response:
        result = response.read().decode('utf-8')
        print("\n✅ SUCCESS! Claim submitted successfully!")
        print("Status Code:", response.status)
        print("Response:", result)
        
        # Check if claim was saved to database
        print("\n📊 Checking database...")
        import pandas as pd
        try:
            df = pd.read_csv("database/claims.csv")
            print(f"Total claims in database: {len(df)}")
            print("Latest 2 claims:")
            print(df.tail(2)[['claim_id', 'claim_amount', 'user_phone', 'garage_id', 'submission_date']].to_string())
        except Exception as e:
            print(f"Error reading database: {e}")
            
except Exception as e:
    print(f"❌ ERROR: {e}")
    print("\n🔧 Troubleshooting:")
    print("1. Make sure backend is running on http://localhost:8000")
    print("2. Check if the /predict endpoint exists")
    print("3. Verify the data structure matches the backend schema")
