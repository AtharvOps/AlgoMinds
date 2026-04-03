def detect_anomaly(data):
    risk = 0
    reasons = []

    if data["claim_amount"] > 5 * data["repair_estimate"]:
        risk += 40
        reasons.append("Abnormal claim ratio")

    return risk, reasons