import pandas as pd
from ml.retrain import retrain_model

def check_and_retrain():
    df = pd.read_csv("database/claims_db.csv")

    if len(df) > 10:
        retrain_model()
        return "Retrained"

    return "Not enough data"