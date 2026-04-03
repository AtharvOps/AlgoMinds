def analyze_image(data):
    risk = 0
    reasons = []

    if data.get("image_uploaded", 0) == 0:
        risk += 20
        reasons.append("No image uploaded")

    if data.get("damage_consistency", 1) == 0:
        risk += 50
        reasons.append("Damage mismatch with claim")

    return risk, reasons