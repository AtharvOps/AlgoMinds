from fastapi import APIRouter
import pandas as pd
import uuid
from app.core.security import hash_password

router = APIRouter()

@router.post("/register")
def register(data: dict):
    user_id = str(uuid.uuid4())

    data["user_id"] = user_id
    data["password"] = hash_password(data["password"])

    df = pd.DataFrame([data])
    df.to_csv("database/users.csv", mode='a', header=False, index=False)

    return {"msg": "User registered"}