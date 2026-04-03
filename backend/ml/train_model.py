import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import pickle

data = pd.read_csv("database/vehicle_claims.csv")

# Feature engineering
data["claim_ratio"] = data["claim_amount"] / (data["repair_estimate"] + 1)
data["high_claim"] = (data["claim_amount"] > 100000).astype(int)
data["frequent_user"] = (data["previous_claims"] > 3).astype(int)

X = data.drop(["is_fraud"], axis=1)
y = data["is_fraud"]

X = pd.get_dummies(X)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = RandomForestClassifier(n_estimators=300)
model.fit(X_scaled, y)

# Save
pickle.dump(model, open("ml/model.pkl", "wb"))
pickle.dump(scaler, open("ml/scaler.pkl", "wb"))
pickle.dump(list(X.columns), open("ml/columns.pkl", "wb"))

print("✅ Model trained!")