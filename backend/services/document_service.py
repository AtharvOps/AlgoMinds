def verify_document(data):
    risk = 0
    reasons = []

    if data.get("document_verified", 1) == 0:
        risk += 40
        reasons.append("Document not verified")

    if data.get("claim_amount", 0) > 200000:
        risk += 20
        reasons.append("High claim with suspicious document")

    return risk, reasons