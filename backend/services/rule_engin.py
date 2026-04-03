def apply_rules(data):
    risk = 0
    reasons = []

    if data["claim_amount"] > 300000:
        risk += 30
        reasons.append("Very high claim amount")

    if data["previous_claims"] > 4:
        risk += 25
        reasons.append("Too many previous claims")

    if data["policy_duration"] < 1:
        risk += 20
        reasons.append("New policy with claim")

    return risk, reasons