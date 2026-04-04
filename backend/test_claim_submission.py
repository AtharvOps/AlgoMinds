import urllib.request
import json

# Test claim submission
test_claim = {
    "claim_amount": 50000,
    "repair_estimate": 30000,
    "previous_claims": 2,
    "policy_validity": 12,
    "image_uploaded": 0,
    "damage_consistency": 1,
    "user_phone": "1234567890",
    "garage_id": "GAR001",
    "agent_id": "AG001",
    "garage_city": "Mumbai",
    "accident_location": "Mumbai"
}

try:
    data = json.dumps(test_claim).encode('utf-8')
    req = urllib.request.Request("http://localhost:8000/predict", data=data, headers={'Content-Type': 'application/json'})
    
    with urllib.request.urlopen(req) as response:
        result = response.read().decode('utf-8')
        print("Status Code:", response.status)
        print("Response:", result)
        
        # Check if claim was saved to database
        print("\nChecking database...")
        import pandas as pd
        try:
            df = pd.read_csv("database/claims_db.csv")
            print(f"Total claims in database: {len(df)}")
            if len(df) > 0:
                print("Last claim:")
                print(df.tail(1).to_string())
        except Exception as e:
            print(f"Error reading database: {e}")
            
except Exception as e:
    print("Error:", e)
