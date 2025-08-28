from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request, Response
from app.routes import leave, auth
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Leave Approval System API", version="1.0.0")

# AMP Email CORS Middleware
@app.middleware("http")
async def add_amp_cors_headers(request: Request, call_next):
    response = await call_next(request)
    
    # Add AMP-specific CORS headers
    if request.url.path.startswith("/leave/"):
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "*"
        response.headers["Access-Control-Expose-Headers"] = "*"
        response.headers["AMP-Access-Control-Allow-Source-Origin"] = request.headers.get("Origin", "*")
        response.headers["Access-Control-Allow-Credentials"] = "true"
    
    return response

# Get URLs from environment for CORS configuration
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

# Enhanced CORS configuration for AMP emails
# Based on working configuration that properly handles AMP email rendering
origins = [
    # Development origins
    "http://localhost:3000",
    "http://localhost:5173",  # Vite default port
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
    # Google/Gmail AMP email origins
    "https://mail.google.com",
    "https://gmail.com", 
    "https://amp.gmail.dev",
    # Google domains pattern support
    "https://accounts.google.com",
    "https://mail.google.com",
    "https://googlemail.com",
    # Production frontend URL from environment
    FRONTEND_URL,
]

# Remove duplicates and None values
origins = list(set(filter(None, origins)))

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=[
        "Content-Type",
        "Authorization", 
        "X-Requested-With",
        "Accept",
        "Origin",
        "AMP-CORS-REQUEST-HEADERS",  # Critical for AMP emails
        "AMP-Same-Origin",           # Critical for AMP emails
        "*"  # Allow all headers for AMP compatibility
    ],
    expose_headers=[
        "AMP-Access-Control-Allow-Source-Origin",
        "AMP-CORS-REQUEST-HEADERS",
        "Access-Control-Expose-Headers",
        "*"  # Expose all headers for AMP compatibility
    ],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(leave.router, prefix="/leave", tags=["leave"])

@app.get("/")
def root():
    return {"message": "Leave Application System API", "version": "1.0.0"}
