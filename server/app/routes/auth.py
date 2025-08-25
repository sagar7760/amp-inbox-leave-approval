from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.models.db import users_collection
from app.models.schemas import Token, UserCreate
from app.utils.auth import verify_password, get_password_hash, create_access_token, verify_token
from bson import ObjectId
from datetime import timedelta
import os

router = APIRouter()

@router.post("/register")
def register_user(user_data: UserCreate):
    # Check if user already exists
    if users_collection.find_one({"email": user_data.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    if users_collection.find_one({"username": user_data.username}):
        raise HTTPException(status_code=400, detail="Username already taken")
    
    # Create user document
    user_dict = {
        "username": user_data.username,
        "email": user_data.email,
        "hashed_password": get_password_hash(user_data.password),
        "full_name": user_data.full_name,
        "role": user_data.role,
        "department": user_data.department,
        "is_manager": user_data.role == "manager",
        "is_hr": user_data.role == "hr"
    }
    
    result = users_collection.insert_one(user_dict)
    return {"user_id": str(result.inserted_id), "message": "User registered successfully"}

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Try to find user by username or email
    user = users_collection.find_one({
        "$or": [
            {"username": form_data.username},
            {"email": form_data.username}
        ]
    })
    
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Incorrect username/email or password")
    
    access_token = create_access_token(
        data={"sub": str(user["_id"]), "email": user["email"]},
        expires_delta=timedelta(minutes=60*24)
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me")
def get_current_user(user_id: str = Depends(verify_token)):
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Return user data without password
    user_data = {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        "full_name": user["full_name"],
        "role": user["role"],
        "department": user["department"],
        "is_manager": user.get("is_manager", False),
        "is_hr": user.get("is_hr", False)
    }
    
    return user_data

@router.post("/test-email")
def test_email():
    """Test endpoint to verify email configuration"""
    try:
        from app.utils.email import send_leave_action_email
        
        # Create test leave data
        test_leave = {
            "employee_name": "Test Employee",
            "manager_email": "sagarsoradi011@gmail.com",  # Send to your own email for testing
            "leave_type": "Annual Leave",
            "start_date": "2025-09-01",
            "end_date": "2025-09-03",
            "reason": "Family vacation - This is a test email"
        }
        
        send_leave_action_email(test_leave)
        return {"message": "Test email sent successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Email test failed: {str(e)}")
