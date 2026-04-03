def generate_explanation(reasons_list):
    reasons = []

    for r in reasons_list:
        reasons.extend(r)

    return list(set(reasons))