def analyze_image(data):
    risk = 0
    reasons = []

    if data.get("image_uploaded", 1) == 0:
        risk += 30
        reasons.append("No image uploaded")

    if data.get("damage_consistency", 1) == 0:
        risk += 50
        reasons.append("Damage inconsistent with claim")

    return risk, reasons