from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid
from services.user_service import save_user, authenticate_user, get_all_users, get_user_statistics

router = APIRouter()

class UserRegister(BaseModel):
    username: str
    email: str
    password: str
    full_name: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[str] = "user"

class UserLogin(BaseModel):
    email: str
    password: str

@router.post("/register")
def register_user(user: UserRegister):
    """
    Register a new user
    """
    try:
        # Generate user ID
        user_data = user.dict()
        user_data['user_id'] = str(uuid.uuid4())
        
        # Save user to database
        result = save_user(user_data)
        
        if result["success"]:
            return {
                "message": "User registered successfully",
                "user_id": user_data['user_id'],
                "username": user_data['username']
            }
        else:
            raise HTTPException(status_code=400, detail=result["message"])
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login")
def login_user(user: UserLogin):
    """
    Authenticate user login
    """
    try:
        result = authenticate_user(user.email, user.password)
        
        if result["success"]:
            return {
                "message": "Login successful",
                "user": result["user"],
                "token": f"token_{result['user']['user_id']}"  # Simple token for demo
            }
        else:
            raise HTTPException(status_code=401, detail=result["message"])
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/users")
def get_users():
    """
    Get all users (admin only)
    """
    try:
        users_df = get_all_users()
        
        if users_df.empty:
            return {"users": [], "total": 0}
        
        users = users_df.to_dict('records')
        return {"users": users, "total": len(users)}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats")
def get_user_stats():
    """
    Get user statistics
    """
    try:
        stats = get_user_statistics()
        return stats
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/test")
def test_auth():
    """
    Test authentication endpoint
    """
    return {"message": "Authentication API working ✅"}