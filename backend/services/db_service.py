import pandas as pd

def check_identity(data):
    df = pd.read_csv("database/vehicle_claims.csv")

    risk = 0
    reasons = []

    matches = df[df["user_phone"] == data["user_phone"]]

    if len(matches) > 3:
        risk += 40
        reasons.append("Multiple claims from same phone")

    return risk, reasons