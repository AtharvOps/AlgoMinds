from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints.predict import router
from app.api.v1.endpoints.admin import router as admin_router
from app.api.v1.endpoints.collusion import router as collusion_router
from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.claims import router as claims_router

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "API running 🚀"}

# include router
app.include_router(router)
app.include_router(admin_router, prefix="/admin")
app.include_router(collusion_router, prefix="/admin")
app.include_router(auth_router, prefix="/auth")
app.include_router(claims_router)