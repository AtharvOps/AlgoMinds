import pandas as pd
import os

def save_claim(data):
    file = "database/claims_db.csv"

    df = pd.DataFrame([data])

    if not os.path.exists(file):
        df.to_csv(file, index=False)
    else:
        df.to_csv(file, mode='a', header=False, index=False)