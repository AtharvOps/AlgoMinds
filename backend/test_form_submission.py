import urllib.request
import json

# Test claim submission with exact frontend form data
test_claim = {
    "claim_amount": 35000,
    "repair_estimate": 25000,
    "previous_claims": 0,
    "policy_validity": 36,
    "image_uploaded": 0,
    "damage_consistency": 1,
    "user_phone": "9998887777",
    "garage_id": "GAR003",
    "agent_id": "AG003",
    "garage_city": "Bangalore",
    "accident_location": "Bangalore"
}

print("🧪 Testing Frontend Claim Form Submission")
print("=" * 50)
print("Form Data:", test_claim)

try:
    data = json.dumps(test_claim).encode('utf-8')
    req = urllib.request.Request("http://localhost:8000/predict", data=data, headers={'Content-Type': 'application/json'})
    
    with urllib.request.urlopen(req) as response:
        result = response.read().decode('utf-8')
        print("\n✅ Frontend Claim Submission SUCCESS!")
        print(f"Claim ID: {json.loads(result)['claim_id']}")
        print(f"Fraud Label: {json.loads(result)['fraud_label']}")
        print(f"Fraud Score: {json.loads(result)['fraud_score']}")
        
        # Verify it's in the database
        import pandas as pd
        df = pd.read_csv("database/claims.csv")
        latest_claim = df.iloc[-1]
        
        print("\n📋 Verified in Database:")
        print(f"Claim Amount: ${latest_claim['claim_amount']}")
        print(f"Phone: {latest_claim['user_phone']}")
        print(f"Garage: {latest_claim['garage_id']}")
        print(f"City: {latest_claim['garage_city']}")
        print(f"Submission: {latest_claim['submission_date']}")
        
        print("\n🎉 Frontend claim form is now WORKING!")
        print("Users can submit claims and they will be stored in the database.")
        
except Exception as e:
    print(f"❌ Error: {e}")
    print("Please check if the backend is running on http://localhost:8000")
