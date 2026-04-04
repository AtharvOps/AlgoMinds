from fastapi import APIRouter
from app.core.pipeline import fraud_pipeline
from app.schemas.claims_schema import ClaimRequest

router = APIRouter()

@router.get("/test")
def test():
    return {"message": "Predict API working ✅"}

@router.post("/predict")
def predict(data: ClaimRequest):
    return fraud_pipeline(data.dict())