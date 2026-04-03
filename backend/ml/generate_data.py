import pandas as pd
import random

rows = []

garages = ["G001", "G002", "G003"]
agents = ["A10", "A11", "A12"]
cities = ["Pune", "Mumbai", "Delhi"]

for i in range(1000):

    claim_id = f"V{i}"
    user_id = f"U{i}"

    # Identity fraud
    user_phone = 9999999999 if i % 50 == 0 else random.randint(9000000000, 9999999999)

    vehicle_type = random.choice(["car", "bike"])
    vehicle_age = random.randint(1, 10)
    policy_duration = random.randint(1, 5)
    previous_claims = random.randint(0, 6)

    accident_type = random.choice(["minor", "major"])
    accident_severity = random.choice(["low", "medium", "high"])

    repair_estimate = random.randint(5000, 100000)

    # Bias collusion
    garage_id = random.choices(["G001","G002","G003"], weights=[0.3,0.5,0.2])[0]
    agent_id = random.choices(["A10","A11","A12"], weights=[0.3,0.5,0.2])[0]

    garage_city = random.choice(cities)
    accident_location = random.choice(cities)

    agent_phone = random.randint(9000000000, 9999999999)

    document_verified = random.choice([0, 1])

    # 🆕 Image features
    image_uploaded = random.choice([0, 1])
    damage_consistency = random.choice([0, 1])

    days_to_claim = random.randint(1, 10)
    claim_freq = random.randint(0, 5)

    fraud = 0

    # ---------- Balanced Fraud Logic ----------

    # Inflation
    if random.random() < 0.25:
        claim_amount = repair_estimate * random.randint(3, 8)
        fraud = 1
    else:
        claim_amount = repair_estimate + random.randint(0, 20000)

    # Behavioral
    if previous_claims > 4 and random.random() < 0.6:
        fraud = 1

    # Document fraud
    if document_verified == 0 and random.random() < 0.7:
        fraud = 1

    # Image fraud
    if damage_consistency == 0 and random.random() < 0.7:
        fraud = 1

    # Collusion (STRONG)
    if garage_id == "G002" and agent_id == "A11":
        fraud = 1
        claim_amount = repair_estimate * random.randint(4, 10)

    # Location fraud
    if garage_city != accident_location and random.random() < 0.5:
        fraud = 1

    rows.append({
        "claim_id": claim_id,
        "user_id": user_id,
        "user_phone": user_phone,
        "vehicle_type": vehicle_type,
        "vehicle_age": vehicle_age,
        "policy_duration": policy_duration,
        "previous_claims": previous_claims,
        "accident_type": accident_type,
        "accident_severity": accident_severity,
        "claim_amount": claim_amount,
        "repair_estimate": repair_estimate,
        "garage_id": garage_id,
        "garage_city": garage_city,
        "agent_id": agent_id,
        "agent_phone": agent_phone,
        "document_verified": document_verified,
        "image_uploaded": image_uploaded,
        "damage_consistency": damage_consistency,
        "accident_location": accident_location,
        "days_to_claim": days_to_claim,
        "claim_frequency_30d": claim_freq,
        "is_fraud": fraud
    })

df = pd.DataFrame(rows)
df.to_csv("../database/vehicle_claims.csv", index=False)

print("✅ Dataset generated!")