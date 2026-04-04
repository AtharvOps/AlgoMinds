from services.ml_services import predict_ml
from services.anomaly_service import detect_anomaly
from services.rule_engin import apply_rules
from services.image_service import analyze_image
from services.identity_services import check_identity
from services.graph_service import check_collusion
from services.inflation_service import check_inflation
from services.scoring_service import calculate_score
from services.explanation_service import generate_explanation
from services.db_service import save_claim

import uuid

def fraud_pipeline(data):

    # Auto IDs
    data["claim_id"] = str(uuid.uuid4())
    data["user_id"] = str(uuid.uuid4())

    scores = []
    reasons = []

    # ML
    ml_prob = predict_ml(data)
    scores.append(int(ml_prob * 100))
    reasons.append([f"ML probability: {round(ml_prob,2)}"])

    # Rules
    r_score, r_reason = apply_rules(data)
    scores.append(r_score)
    reasons.append(r_reason)

    # Image
    i_score, i_reason = analyze_image(data)
    scores.append(i_score)
    reasons.append(i_reason)

    # Identity
    id_score, id_reason = check_identity(data)
    scores.append(id_score)
    reasons.append(id_reason)

    # Collusion
    g_score, g_reason = check_collusion(data)
    scores.append(g_score)
    reasons.append(g_reason)

    # Inflation
    infl_score, infl_reason = check_inflation(data)
    scores.append(infl_score)
    reasons.append(infl_reason)

    # Anomaly
    a_score, a_reason = detect_anomaly(data)
    scores.append(a_score)
    reasons.append(a_reason)

    # Final decision
    label, total = calculate_score(scores)
    explanation = generate_explanation(reasons)

    data["is_fraud"] = 1 if label == "HIGH FRAUD" else 0

    # Save to CSV
    save_claim(data)

    return {
        "claim_id": data["claim_id"],
        "fraud_label": label,
        "fraud_score": total,
        "reasons": explanation
    }