def check_inflation(data):
    ratio = data["claim_amount"] / (data["repair_estimate"] + 1)

    if ratio > 5:
        return 50, ["Claim amount inflated"]

    return 0, []