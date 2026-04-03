from fastapi import FastAPI
from api.v1.endpoints.predict import router

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API is running 🚀"}

app.include_router(router)