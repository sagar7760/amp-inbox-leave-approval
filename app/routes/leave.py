from fastapi import APIRouter, HTTPException, Depends, Request, status
from app.models.db import leaves_collection, users_collection
from app.models.schemas import LeaveRequest
from app.utils.auth import verify_token, verify_password
from app.utils.email import send_leave_action_email, notify_employee
from bson import ObjectId
from datetime import datetime, timezone
from typing import Optional

router = APIRouter()

from fastapi import APIRouter, HTTPException, Depends, Request, status
from app.models.db import leaves_collection, users_collection
from app.models.schemas import LeaveRequestCreate, LeaveRequest, LeaveActionRequest
from app.utils.auth import verify_token, verify_password
from app.utils.email import send_leave_action_email, notify_employee
from bson import ObjectId
from datetime import datetime, timezone
from typing import Optional, List

router = APIRouter()

@router.post("/submit")
def submit_leave(leave: LeaveRequestCreate, user_id: str = Depends(verify_token)):
    # Get user details
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Find manager by email
    manager = users_collection.find_one({"email": leave.manager_email})
    if not manager:
        raise HTTPException(status_code=404, detail="Manager not found")
    
    # Create leave request
    leave_dict = leave.model_dump()
    leave_dict.update({
        "employee_id": ObjectId(user_id),
        "manager_id": ObjectId(manager["_id"]),
        "status": "pending",
        "is_action_taken": False,
        "created_at": datetime.now(timezone.utc).isoformat()
    })
    
    result = leaves_collection.insert_one(leave_dict)
    
    # Send AMP email to manager
    leave_dict["_id"] = result.inserted_id
    send_leave_action_email(leave_dict)
    
    return {"leave_request_id": str(result.inserted_id), "status": "pending"}

@router.get("/my-requests", response_model=List[dict])
def get_my_requests(user_id: str = Depends(verify_token)):
    leaves = list(leaves_collection.find({"employee_id": ObjectId(user_id)}))
    for leave in leaves:
        leave["_id"] = str(leave["_id"])
        leave["employee_id"] = str(leave["employee_id"])
        leave["manager_id"] = str(leave["manager_id"])
        if leave.get("approver_id"):
            leave["approver_id"] = str(leave["approver_id"])
    return leaves

@router.get("/pending-approvals", response_model=List[dict])
def get_pending_approvals(user_id: str = Depends(verify_token)):
    # Check if user is a manager
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if not user or not user.get("is_manager"):
        raise HTTPException(status_code=403, detail="Access denied. Manager role required.")
    
    leaves = list(leaves_collection.find({
        "manager_id": ObjectId(user_id), 
        "status": "pending",
        "is_action_taken": False
    }))
    
    for leave in leaves:
        leave["_id"] = str(leave["_id"])
        leave["employee_id"] = str(leave["employee_id"])
        leave["manager_id"] = str(leave["manager_id"])
        if leave.get("approver_id"):
            leave["approver_id"] = str(leave["approver_id"])
    return leaves

@router.post("/{leave_id}/approve")
def approve_leave(leave_id: str, action_data: LeaveActionRequest):
    return process_leave_action(leave_id, "approved", action_data.manager_password, action_data.comments)

@router.post("/{leave_id}/reject") 
def reject_leave(leave_id: str, action_data: LeaveActionRequest):
    return process_leave_action(leave_id, "rejected", action_data.manager_password, action_data.comments)

def process_leave_action(leave_id: str, action: str, password: str, comments: Optional[str] = None):
    # Find leave request
    leave = leaves_collection.find_one({"_id": ObjectId(leave_id)})
    if not leave:
        raise HTTPException(status_code=404, detail="Leave request not found")
    
    if leave.get("is_action_taken"):
        raise HTTPException(status_code=400, detail="Action already taken on this leave request")
    
    # Verify manager password
    manager = users_collection.find_one({"_id": ObjectId(leave["manager_id"])})
    if not manager or not verify_password(password, manager["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid manager password")
    
    # Update leave status
    update_data = {
        "status": action,
        "is_action_taken": True,
        "approver_id": ObjectId(leave["manager_id"]),
        "action_timestamp": datetime.now(timezone.utc).isoformat()
    }
    
    if comments:
        update_data["comments"] = comments
    
    leaves_collection.update_one({"_id": ObjectId(leave_id)}, {"$set": update_data})
    
    # Notify employee
    notify_employee(leave, action)
    
    return {
        "status": action,
        "message": f"Leave request {action} successfully.",
        "comments": comments
    }
