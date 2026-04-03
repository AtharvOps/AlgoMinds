def calculate_score(scores):
    total = sum(scores)

    if total > 150:
        return "HIGH FRAUD", total
    elif total > 80:
        return "MEDIUM FRAUD", total
    else:
        return "LOW RISK", total