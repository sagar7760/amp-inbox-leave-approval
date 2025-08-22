import os
from email.message import EmailMessage
import smtplib
from jinja2 import Environment, FileSystemLoader
from dotenv import load_dotenv

load_dotenv()

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

env = Environment(loader=FileSystemLoader("app/utils/templates"))

def send_leave_action_email(leave_dict):
    # Render AMP email with embedded form
    template = env.get_template("leave_action.amp.html")
    html_content = template.render(leave=leave_dict)
    msg = EmailMessage()
    msg["Subject"] = "Leave Approval Request"
    msg["From"] = EMAIL_USER
    msg["To"] = ",".join([leave_dict["manager_email"], leave_dict.get("hr_email", "")])
    msg.set_content("This is an AMP email. Please use a compatible client.")
    msg.add_alternative(html_content, subtype="x-amp-html")
    with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)

def notify_employee(leave, action):
    # Notify employee of status change
    pass  # Implement as needed
