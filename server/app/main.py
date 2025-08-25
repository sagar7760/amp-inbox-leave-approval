from fastapi import FastAPI
from app.routes import leave, auth

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(leave.router, prefix="/leave", tags=["leave"])

@app.get("/")
def root():
    return {"message": "Leave Application System API"}
