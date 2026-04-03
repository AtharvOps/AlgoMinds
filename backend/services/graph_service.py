import pandas as pd

def check_collusion(data):
    df = pd.read_csv("database/vehicle_claims.csv")

    risk = 0
    reasons = []

    suspicious = df[
        (df["garage_id"] == data["garage_id"]) &
        (df["agent_id"] == data["agent_id"]) &
        (df["is_fraud"] == 1)
    ]

    if len(suspicious) > 5:
        risk += 50
        reasons.append("Linked to fraud network (garage-agent)")

    return risk, reasons