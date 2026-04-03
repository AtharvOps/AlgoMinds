import pickle
import pandas as pd

# Load trained artifacts
model = pickle.load(open("ml/model.pkl", "rb"))
scaler = pickle.load(open("ml/scaler.pkl", "rb"))
columns = pickle.load(open("ml/columns.pkl", "rb"))


def predict_ml(data: dict):

    # Convert input → DataFrame
    df = pd.DataFrame([data])

    # =========================
    # FEATURE ENGINEERING (MUST MATCH TRAINING)
    # =========================

    # Safe handling (avoid crash)
    df["repair_estimate"] = df.get("repair_estimate", 0)
    df["claim_amount"] = df.get("claim_amount", 0)
    df["previous_claims"] = df.get("previous_claims", 0)

    df["claim_ratio"] = df["claim_amount"] / (df["repair_estimate"] + 1)
    df["high_claim"] = (df["claim_amount"] > 100000).astype(int)
    df["frequent_user"] = (df["previous_claims"] > 3).astype(int)

    # Location mismatch
    df["garage_city"] = df.get("garage_city", "")
    df["accident_location"] = df.get("accident_location", "")
    df["location_mismatch"] = (df["garage_city"] != df["accident_location"]).astype(int)

    # =========================
    # DROP UNUSED FIELDS (IMPORTANT)
    # =========================

    drop_cols = [
        "claim_id",
        "user_id",
        "user_phone",
        "aadhar_number",
        "chassis_number",
        "policy_number"
    ]

    for col in drop_cols:
        if col in df:
            df = df.drop(col, axis=1)

    # =========================
    # ENCODING (same as training)
    # =========================

    df = pd.get_dummies(df)

    # =========================
    # COLUMN MATCHING (CRITICAL)
    # =========================

    for col in columns:
        if col not in df:
            df[col] = 0

    df = df[columns]

    # =========================
    # SCALING
    # =========================

    df_scaled = scaler.transform(df)

    # =========================
    # PREDICTION
    # =========================

    prob = model.predict_proba(df_scaled)[0][1]

    return prob