import pickle
import pandas as pd

model = pickle.load(open("ml/model.pkl", "rb"))
scaler = pickle.load(open("ml/scaler.pkl", "rb"))
columns = pickle.load(open("ml/columns.pkl", "rb"))

def predict_ml(data: dict):
    df = pd.DataFrame([data])

    # Feature Engineering (same as training)
    df["claim_ratio"] = df["claim_amount"] / (df["repair_estimate"] + 1)
    df["high_claim"] = (df["claim_amount"] > 100000).astype(int)
    df["frequent_user"] = (df["previous_claims"] > 3).astype(int)
    df["location_mismatch"] = (df["garage_city"] != df["accident_location"]).astype(int)

    df["collusion_flag"] = (
        (df["garage_id"] == "G002") &
        (df["agent_id"] == "A11")
    ).astype(int)

    df["doc_risk"] = (df["document_verified"] == 0).astype(int)
    df["image_risk"] = (df["damage_consistency"] == 0).astype(int)

    df = pd.get_dummies(df)

    # Match columns
    for col in columns:
        if col not in df:
            df[col] = 0

    df = df[columns]

    df_scaled = scaler.transform(df)

    prob = model.predict_proba(df_scaled)[0][1]

    return prob