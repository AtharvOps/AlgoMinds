def verify_document(data):
    risk = 0
    reasons = []

    if data.get("document_verified", 1) == 0:
        risk += 40
        reasons.append("Documents not verified")

    return risk, reasons