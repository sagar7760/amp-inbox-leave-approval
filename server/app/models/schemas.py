from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, Annotated
from bson import ObjectId
from datetime import datetime

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")

class User(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )
    
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    email: EmailStr
    hashed_password: str
    full_name: str
    is_manager: bool = False
    is_hr: bool = False

class LeaveRequestCreate(BaseModel):
    start_date: str
    end_date: str
    leave_type: str
    reason: str
    manager_email: str

class LeaveRequest(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )
    
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    employee_id: Optional[PyObjectId] = None
    manager_id: Optional[PyObjectId] = None
    start_date: str
    end_date: str
    leave_type: str
    reason: str
    manager_email: str
    status: str = "pending"
    is_action_taken: bool = False
    approver_id: Optional[PyObjectId] = None
    action_timestamp: Optional[str] = None
    created_at: Optional[str] = None

class LeaveActionRequest(BaseModel):
    comments: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: str
    role: str = "employee"
    department: str

class ApprovalToken(BaseModel):
    token: str
    leave_id: str
    manager_id: str
    action: str  # "approve" or "reject"
    expires_at: datetime
    is_used: bool = False
    created_at: datetime
