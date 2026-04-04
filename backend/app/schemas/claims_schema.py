from pydantic import BaseModel
from typing import Optional

class ClaimRequest(BaseModel):
    claim_amount: float
    repair_estimate: float
    previous_claims: int
    policy_validity: int
    image_uploaded: int
    damage_consistency: int
    user_phone: Optional[str] = None
    aadhar_number: Optional[str] = None
    garage_id: Optional[str] = None
    agent_id: Optional[str] = None
    garage_city: Optional[str] = None
    accident_location: Optional[str] = None