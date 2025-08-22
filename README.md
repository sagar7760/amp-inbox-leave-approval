# FastAPI Leave Application System

This backend project provides a secure, high-performance leave application system using FastAPI, MongoDB, and AMP for Email. It is designed for easy deployment to Heroku.

## Features
- Token-based authentication for employees and managers
- Leave request submission and status tracking
- AMP email integration for in-inbox approval/rejection
- Secure password verification for approvers
- Prevention of duplicate/conflicting actions
- MongoDB for robust data persistence
- Ready for Heroku deployment

## Setup
1. Clone the repository
2. Set up environment variables (see `.env.example`)
3. Install dependencies: `pip install -r requirements.txt`
4. Run the app: `uvicorn app.main:app --reload`

## Deployment
- Includes `Procfile` for Heroku deployment

## Directory Structure
- `app/` - FastAPI application code
- `app/models/` - Pydantic and DB models
- `app/routes/` - API endpoints
- `app/utils/` - Utility functions (email, auth, etc.)

## License
MIT
