import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import pickle

def retrain_model():
    print("🔄 Retraining started...")

    df1 = pd.read_csv("database/vehicle_claims.csv")
    df2 = pd.read_csv("database/claims_db.csv")

    # Use only verified data
    df2 = df2[df2["fraud_verified"].notnull()]

    # Combine
    data = pd.concat([df1, df2], ignore_index=True)

    # Feature Engineering
    data["claim_ratio"] = data["claim_amount"] / (data["repair_estimate"] + 1)
    data["high_claim"] = (data["claim_amount"] > 100000).astype(int)
    data["frequent_user"] = (data["previous_claims"] > 3).astype(int)
    data["location_mismatch"] = (data["garage_city"] != data["accident_location"]).astype(int)

    X = data.drop(["is_fraud", "fraud_verified"], axis=1, errors="ignore")
    y = data["is_fraud"]

    X = pd.get_dummies(X)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = RandomForestClassifier(n_estimators=300)
    model.fit(X_scaled, y)

    pickle.dump(model, open("ml/model.pkl", "wb"))
    pickle.dump(scaler, open("ml/scaler.pkl", "wb"))
    pickle.dump(list(X.columns), open("ml/columns.pkl", "wb"))

    print("✅ Model retrained successfully!")