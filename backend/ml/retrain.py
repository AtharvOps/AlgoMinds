import pandas as pd
from ml.train_model import *

def retrain_model():
    print("🔄 Retraining using new data...")

    df1 = pd.read_csv("database/vehicle_claims.csv")
    df2 = pd.read_csv("database/claims_db.csv")

    data = pd.concat([df1, df2], ignore_index=True)

    data.to_csv("database/vehicle_claims.csv", index=False)

    print("✅ Dataset updated. Run train_model again.")