def calculate_score(scores):
    total = sum(scores)

    if total > 180:
        return "HIGH FRAUD", total
    elif total > 100:
        return "MEDIUM FRAUD", total
    else:
        return "LOW RISK", total