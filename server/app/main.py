from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import leave, auth

app = FastAPI(title="Leave Approval System API", version="1.0.0")

# Configure CORS
origins = [
    "http://localhost:5173",  # Vite default port
    "http://localhost:3000",  # React default port
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
    # Allow email clients to submit AMP forms
    "https://mail.google.com",
    "*",  # Allow all origins for AMP email compatibility (be cautious in production)
    # Add your Heroku frontend URL here when deployed
    # "https://your-frontend-app.herokuapp.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(leave.router, prefix="/leave", tags=["leave"])

@app.get("/")
def root():
    return {"message": "Leave Application System API", "version": "1.0.0"}
