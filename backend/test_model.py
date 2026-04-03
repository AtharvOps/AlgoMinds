import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.ml_services import predict_ml

sample = {
    "claim_amount": 300000,
    "repair_estimate": 10000,
    "previous_claims": 5,
    "garage_city": "Pune",
    "accident_location": "Mumbai"
}

print("Fraud Probability:", predict_ml(sample))