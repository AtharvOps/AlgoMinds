import sys
import os

# Change the path to the parent directory to access the 'services' module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.ml_service import predict_ml

sample = {
    "claim_amount": 300000,
    "repair_estimate": 10000,
    "previous_claims": 5,
    "garage_city": "Pune",
    "accident_location": "Mumbai"
}

print("Fraud Probability:", predict_ml(sample))