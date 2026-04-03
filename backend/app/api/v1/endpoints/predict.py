from fastapi import APIRouter
from app.core.pipeline import fraud_pipeline

router = APIRouter()

@router.get("/")
def test():
    return {"message": "Predict API working ✅"}

@router.post("/predict")
def predict(data: dict):
    return fraud_pipeline(data)