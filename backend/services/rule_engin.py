def apply_rules(data):
    risk = 0
    reasons = []

    if data["claim_amount"] > 300000:
        risk += 30
        reasons.append("Very high claim amount")

    if data["previous_claims"] > 4:
        risk += 25
        reasons.append("Frequent claimant")

    if data["policy_validity"] < 1:
        risk += 40
        reasons.append("Policy expired")

    return risk, reasons