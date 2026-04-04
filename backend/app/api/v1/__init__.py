def check_inflation(data):
    risk = 0
    reasons = []

    ratio = data["claim_amount"] / (data["repair_estimate"] + 1)

    if ratio > 5:
        risk += 50
        reasons.append("Highly inflated claim")
    elif ratio > 3:
        risk += 25
        reasons.append("Moderately inflated claim")

    return risk, reasons

def detect_anomaly(data):
    # Keep the same behavior as existing anomaly check
    return check_inflation(data)