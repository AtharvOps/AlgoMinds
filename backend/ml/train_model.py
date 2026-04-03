import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import pickle

data = pd.read_csv("../database/vehicle_claims.csv")

# 🔥 Feature Engineering
data["claim_ratio"] = data["claim_amount"] / (data["repair_estimate"] + 1)
data["high_claim"] = (data["claim_amount"] > 100000).astype(int)
data["frequent_user"] = (data["previous_claims"] > 3).astype(int)
data["location_mismatch"] = (data["garage_city"] != data["accident_location"]).astype(int)

# Collusion
data["collusion_flag"] = (
    (data["garage_id"] == "G002") &
    (data["agent_id"] == "A11")
).astype(int)

# Document + Image risk
data["doc_risk"] = (data["document_verified"] == 0).astype(int)
data["image_risk"] = (data["damage_consistency"] == 0).astype(int)

X = data.drop([
    "claim_id","user_id","user_phone","agent_phone","is_fraud"
], axis=1)

y = data["is_fraud"]

X = pd.get_dummies(X)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(
    n_estimators=400,
    max_depth=15,
    min_samples_split=4,
    min_samples_leaf=2,
    random_state=42
)

model.fit(X_train, y_train)

print("Train:", model.score(X_train, y_train))
print("Test:", model.score(X_test, y_test))

pickle.dump(model, open("model.pkl","wb"))
pickle.dump(scaler, open("scaler.pkl","wb"))
pickle.dump(list(X.columns), open("columns.pkl","wb"))

print("✅ Model ready!")