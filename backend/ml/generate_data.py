import pandas as pd
import random
import uuid

rows = []

vehicle_types = {
    "car": ["sedan", "SUV", "hatchback", "XUV"],
    "bike": ["sports", "cruiser", "scooty", "classic"]
}

cities = ["Pune", "Mumbai", "Delhi", "Bangalore"]
garages = ["G001", "G002", "G003"]
agents = ["A10", "A11", "A12"]

fraud_garage = "G002"
fraud_agent = "A11"

for i in range(500):

    claim_id = str(uuid.uuid4())
    user_id = str(uuid.uuid4())

    user_phone = random.randint(9000000000, 9999999999)
    aadhar_number = random.randint(100000000000, 999999999999)

    vehicle_type = random.choice(list(vehicle_types.keys()))
    vehicle_subtype = random.choice(vehicle_types[vehicle_type])
    vehicle_age = random.randint(1, 10)
    vehicle_model = f"Model_{random.randint(1,50)}"
    chassis_number = str(uuid.uuid4())[:10]

    policy_number = str(uuid.uuid4())[:8]
    policy_validity = random.randint(1, 5)

    claim_type = random.choice(["accident", "theft"])
    previous_claims = random.randint(0, 6)
    claim_freq = random.randint(0, 5)

    accident_type = random.choice(["minor", "major"])
    accident_severity = random.choice(["low", "medium", "high"])

    accident_location = random.choice(cities)
    garage_city = random.choice(cities)

    garage_id = random.choice(garages)
    agent_id = random.choice(agents)

    repair_estimate = random.randint(5000, 50000)

    document_verified = random.choice([0, 1])
    damage_consistency = random.choice([0, 1])
    image_uploaded = random.choice([0, 1])

    days_to_claim = random.randint(1, 10)

    # =========================
    # FRAUD LOGIC
    # =========================
    fraud = 0

    # Inflation fraud
    if random.random() < 0.3:
        claim_amount = repair_estimate * random.randint(3, 8)
        fraud = 1
    else:
        claim_amount = repair_estimate + random.randint(0, 20000)

    # Frequent claims fraud
    if previous_claims > 4:
        fraud = 1

    # Document fraud
    if document_verified == 0 and claim_amount > 100000:
        fraud = 1

    # Image mismatch fraud
    if damage_consistency == 0 and claim_amount > 80000:
        fraud = 1

    # Collusion fraud
    if garage_id == fraud_garage and agent_id == fraud_agent:
        if random.random() < 0.9:
            fraud = 1
            claim_amount = repair_estimate * random.randint(5, 10)

    # Location mismatch
    if garage_city != accident_location and claim_amount > 150000:
        fraud = 1

    rows.append({
        "claim_id": claim_id,
        "user_id": user_id,
        "user_phone": user_phone,
        "aadhar_number": aadhar_number,
        "vehicle_type": vehicle_type,
        "vehicle_subtype": vehicle_subtype,
        "vehicle_age": vehicle_age,
        "vehicle_model": vehicle_model,
        "chassis_number": chassis_number,
        "policy_number": policy_number,
        "policy_validity": policy_validity,
        "claim_type": claim_type,
        "previous_claims": previous_claims,
        "claim_frequency_30d": claim_freq,
        "accident_type": accident_type,
        "accident_severity": accident_severity,
        "accident_location": accident_location,
        "garage_city": garage_city,
        "claim_amount": claim_amount,
        "repair_estimate": repair_estimate,
        "garage_id": garage_id,
        "agent_id": agent_id,
        "document_verified": document_verified,
        "damage_consistency": damage_consistency,
        "image_uploaded": image_uploaded,
        "days_to_claim": days_to_claim,
        "is_fraud": fraud
    })

df = pd.DataFrame(rows)
df.to_csv("../database/vehicle_claims.csv", index=False)

print("✅ Dataset generated with realistic fraud patterns!")