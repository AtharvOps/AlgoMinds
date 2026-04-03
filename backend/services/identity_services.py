import pandas as pd

def check_identity(data):
    try:
        df = pd.read_csv("database/vehicle_claims.csv")
    except:
        return 0, []

    risk = 0
    reasons = []

    user_phone = data.get("user_phone")

    # 🔥 1. Same phone multiple times
    phone_matches = df[df["user_phone"] == user_phone]

    if len(phone_matches) > 3:
        risk += 40
        reasons.append("Multiple claims linked to same phone number")

    # 🔥 2. Frequent claims behavior
    if data.get("previous_claims", 0) > 4:
        risk += 30
        reasons.append("User has excessive previous claims")

    # 🔥 3. Identity reuse + fraud history
    fraud_matches = phone_matches[phone_matches["is_fraud"] == 1]

    if len(fraud_matches) > 1:
        risk += 50
        reasons.append("Phone linked to previous fraudulent claims")

    return risk, reasons