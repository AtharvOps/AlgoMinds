import pandas as pd

def check_collusion(data):
    risk = 0
    reasons = []

    try:
        df = pd.read_csv("database/claims_db.csv")

        matches = df[
            (df["garage_id"] == data["garage_id"]) &
            (df["agent_id"] == data["agent_id"])
        ]

        if len(matches) > 3:
            risk += 40
            reasons.append("Garage-Agent collusion detected")

    except:
        pass

    return risk, reasons