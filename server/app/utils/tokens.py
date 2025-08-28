import secrets
from datetime import datetime, timedelta, timezone
from app.models.db import tokens_collection
from bson import ObjectId
from typing import Optional

def generate_approval_token(leave_id: str, manager_id: str, action: str = "approve", hours_valid: int = 24) -> str:
    """
    Generate a unique one-time token for leave approval/rejection
    
    Args:
        leave_id: The leave request ID
        manager_id: The manager's user ID
        action: "approve" or "reject"
        hours_valid: How many hours the token is valid (default 24)
    
    Returns:
        The generated token string
    """
    token = secrets.token_urlsafe(32)
    expires_at = datetime.now(timezone.utc) + timedelta(hours=hours_valid)
    
    token_doc = {
        "token": token,
        "leave_id": leave_id,
        "manager_id": manager_id,
        "action": action,
        "expires_at": expires_at,
        "is_used": False,
        "created_at": datetime.now(timezone.utc)
    }
    
    tokens_collection.insert_one(token_doc)
    return token

def verify_token(token: str) -> Optional[dict]:
    """
    Verify if a token is valid and not expired
    
    Args:
        token: The token to verify
    
    Returns:
        Token document if valid, None otherwise
    """
    token_doc = tokens_collection.find_one({
        "token": token,
        "is_used": False,
        "expires_at": {"$gt": datetime.now(timezone.utc)}
    })
    
    return token_doc

def use_token(token: str) -> bool:
    """
    Mark a token as used
    
    Args:
        token: The token to mark as used
    
    Returns:
        True if token was successfully marked as used, False otherwise
    """
    result = tokens_collection.update_one(
        {"token": token, "is_used": False},
        {"$set": {"is_used": True, "used_at": datetime.now(timezone.utc)}}
    )
    
    return result.modified_count > 0

def cleanup_expired_tokens():
    """
    Remove expired tokens from the database
    This should be called periodically (e.g., via a cron job)
    """
    result = tokens_collection.delete_many({
        "expires_at": {"$lt": datetime.now(timezone.utc)}
    })
    
    print(f"Cleaned up {result.deleted_count} expired tokens")
    return result.deleted_count

def revoke_tokens_for_leave(leave_id: str):
    """
    Revoke all tokens for a specific leave request
    Useful when leave is processed through other means
    
    Args:
        leave_id: The leave request ID
    """
    result = tokens_collection.update_many(
        {"leave_id": leave_id, "is_used": False},
        {"$set": {"is_used": True, "revoked_at": datetime.now(timezone.utc)}}
    )
    
    return result.modified_count
