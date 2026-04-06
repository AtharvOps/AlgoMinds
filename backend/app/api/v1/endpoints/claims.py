import csv
from pathlib import Path

from fastapi import APIRouter

router = APIRouter(prefix="/claims", tags=["claims"])


def _claims_csv_path() -> Path:
    # backend/app/api/v1/endpoints -> backend/database/claims.csv
    return Path(__file__).resolve().parents[4] / "database" / "claims.csv"


@router.get("/recent")
def get_recent_claims(limit: int = 10):
    rows = []
    csv_path = _claims_csv_path()

    if not csv_path.exists():
        return {"claims": [], "count": 0}

    with csv_path.open(mode="r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            rows.append(
                {
                    "internalId": row.get("claim_id", ""),
                    "policyNumber": row.get("user_id", ""),
                    "claimDate": (row.get("submission_date", "") or "").split(" ")[0],
                    "ingestionStatus": (row.get("status", "Pending") or "Pending").capitalize(),
                }
            )

    if limit < 1:
        limit = 1

    recent = list(reversed(rows))[:limit]
    return {"claims": recent, "count": len(recent)}
