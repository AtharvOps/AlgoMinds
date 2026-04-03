import pandas as pd

def check_identity(data):
    risk = 0
    reasons = []

    try:
        df = pd.read_csv("database/claims_db.csv")

        # Same phone reuse
        if "user_phone" in df.columns:
            if data["user_phone"] in df["user_phone"].values:
                risk += 20
                reasons.append("Phone reused in multiple claims")

        # Aadhaar reuse
        if "aadhar_number" in df.columns:
            if data["aadhar_number"] in df["aadhar_number"].values:
                risk += 30
                reasons.append("Aadhaar used multiple times")

    except:
        pass

    return risk, reasons