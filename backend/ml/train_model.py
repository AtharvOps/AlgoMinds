import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
import pickle

# Load dataset
data = pd.read_csv("../database/vehicle_claims.csv")

# =========================
# FEATURE ENGINEERING
# =========================

data["claim_ratio"] = data["claim_amount"] / (data["repair_estimate"] + 1)
data["high_claim"] = (data["claim_amount"] > 100000).astype(int)
data["frequent_user"] = (data["previous_claims"] > 3).astype(int)
data["location_mismatch"] = (data["garage_city"] != data["accident_location"]).astype(int)

# =========================
# DROP UNNECESSARY COLUMNS
# =========================

data = data.drop([
    "claim_id",
    "user_id",
    "user_phone",
    "aadhar_number",
    "chassis_number",
    "policy_number"
], axis=1)

# =========================
# SPLIT
# =========================

X = data.drop("is_fraud", axis=1)
y = data["is_fraud"]

# Convert categorical → numeric
X = pd.get_dummies(X)

# Save column structure
columns = X.columns

# Scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

# =========================
# MODEL (IMPROVED)
# =========================

model = RandomForestClassifier(
    n_estimators=200,
    max_depth=12,              # prevents overfitting
    min_samples_split=5,
    min_samples_leaf=3,
    random_state=42
)

model.fit(X_train, y_train)

# =========================
# EVALUATION
# =========================

train_acc = model.score(X_train, y_train)
test_acc = model.score(X_test, y_test)

print("Train Accuracy:", train_acc)
print("Test Accuracy:", test_acc)

y_pred = model.predict(X_test)
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

# =========================
# SAVE MODEL
# =========================

pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(scaler, open("scaler.pkl", "wb"))
pickle.dump(list(columns), open("columns.pkl", "wb"))

print("✅ Model trained & saved!")

feature_importance = pd.Series(model.feature_importances_, index=columns)
print("\nTop Features:\n")
print(feature_importance.sort_values(ascending=False).head(10))