import pandas as pd
from ml.retrain import retrain_model

THRESHOLD = 10  # you can change

def check_and_retrain():
    try:
        df = pd.read_csv("database/claims_db.csv")
    except:
        return "No data"

    # Only verified data
    df = df[df["fraud_verified"].notnull()]

    if len(df) >= THRESHOLD:
        retrain_model()
        return "Retrained"
    
    return f"Current verified data: {len(df)}"