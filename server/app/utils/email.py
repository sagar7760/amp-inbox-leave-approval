import os
from email.message import EmailMessage
import smtplib
from jinja2 import Environment, FileSystemLoader
from dotenv import load_dotenv
from app.utils.tokens import generate_approval_token

load_dotenv()

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

# URL Configuration for deployment
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

env = Environment(loader=FileSystemLoader("app/utils/templates"))

def send_leave_action_email(leave_dict):
    try:
        # Check if email configuration is available
        if not all([EMAIL_HOST, EMAIL_USER, EMAIL_PASS]):
            print("Email configuration not available, skipping email notification")
            return
        
        # Validate URL configuration
        if not BACKEND_URL or not FRONTEND_URL:
            print("URL configuration missing, using default localhost URLs")
            backend_url = "http://localhost:8000"
            frontend_url = "http://localhost:5173"
        else:
            backend_url = BACKEND_URL
            frontend_url = FRONTEND_URL
        
        print(f"Email will use URLs - Backend: {backend_url}, Frontend: {frontend_url}")
        
        # For production, get fresh leave data to show current status in email
        from app.models.db import leaves_collection
        from bson import ObjectId
        
        # Get the latest leave data if _id exists
        if '_id' in leave_dict:
            fresh_leave = leaves_collection.find_one({"_id": ObjectId(leave_dict['_id'])})
            if fresh_leave:
                # Update leave_dict with fresh data
                leave_dict.update(fresh_leave)
                leave_dict['_id'] = str(fresh_leave['_id'])
                leave_dict['manager_id'] = str(fresh_leave['manager_id'])
                leave_dict['employee_id'] = str(fresh_leave['employee_id'])
        
        # Generate one-time tokens for approval and rejection
        leave_id = str(leave_dict['_id'])
        manager_id = str(leave_dict['manager_id'])
        
        # Generate tokens (24 hours validity)
        approval_token = generate_approval_token(leave_id, manager_id, "approve", 24)
        rejection_token = generate_approval_token(leave_id, manager_id, "reject", 24)
        
        # Add tokens to leave_dict for template
        leave_dict['approval_token'] = approval_token
        leave_dict['rejection_token'] = rejection_token
        
        # Add URLs for template
        leave_dict['backend_url'] = backend_url
        leave_dict['frontend_url'] = frontend_url
        
        # Render AMP email with embedded form
        template = env.get_template("leave_action.amp.html")
        html_content = template.render(leave=leave_dict)
        
        msg = EmailMessage()
        msg["Subject"] = f"Leave Request {leave_dict.get('status', 'Approval').title()} - {leave_dict.get('employee_name', 'Employee')}"
        msg["From"] = EMAIL_USER
        msg["To"] = leave_dict["manager_email"]
        msg.set_content("This is an AMP email. Please use a compatible email client to see the interactive form.")
        msg.add_alternative(html_content, subtype="x-amp-html")
        
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
        
        status_text = leave_dict.get('status', 'pending')
        print(f"AMP email notification sent successfully for {status_text} leave request from {leave_dict.get('employee_name', 'Employee')}")
        print(f"Generated tokens - Approval: {approval_token[:8]}..., Rejection: {rejection_token[:8]}...")
        
    except Exception as e:
        # Log the error but don't fail the leave submission
        print(f"Failed to send email notification: {str(e)}")
        print("Leave request was still processed successfully")

def notify_employee(leave, action):
    # Notify employee of status change
    pass  # Implement as needed
