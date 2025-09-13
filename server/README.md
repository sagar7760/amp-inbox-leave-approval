# FastAPI Leave Application System - Backend

This backend project provides a secure, high-performance leave application system using FastAPI, MongoDB, and AMP for Email. It is designed for easy deployment to Heroku.

## Features
- Token-based authentication for employees and managers
- Leave request submission and status tracking
- AMP email integration for in-inbox approval/rejection
- Secure password verification for approvers
- Prevention of duplicate/conflicting actions
- MongoDB for robust data persistence
- Ready for Heroku deployment

## Prerequisites
- Python 3.8+
- MongoDB Atlas account (or local MongoDB instance)
- Gmail account with App Password enabled

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Environment Configuration
Copy the environment template and configure your variables:
```bash
cp .env.example .env
```

Edit `.env` file with your actual values:
```env
# Database Configuration - Replace with your MongoDB Atlas connection string
MONGODB_URI=mongodb+srv://YOUR_USERNAME:YOUR_PASSWORD@YOUR_CLUSTER.mongodb.net/leaveapproval?retryWrites=true&w=majority

# Security - Generate a secure secret key
SECRET_KEY=your-secure-jwt-secret-key-here

# Email Configuration - Use Gmail with App Password
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your-email@gmail.com
EMAIL_PASS=your-gmail-app-password

# URL Configuration
BACKEND_URL=http://localhost:8000
FRONTEND_URL=http://localhost:5173
```

### 3. Environment Variables Setup Guide

#### MongoDB Atlas Setup:
1. Create account at [MongoDB Atlas](https://www.mongodb.com/atlas)
2. Create a new cluster (free tier available)
3. Create database user: Database Access → Add New User
4. Set username/password and save credentials
5. Network Access → Add IP Address → Allow access from anywhere (0.0.0.0/0) for development
6. Connect → Connect your application → Copy connection string
7. Replace `<username>`, `<password>`, and `<cluster>` in connection string

#### Gmail App Password Setup:
1. Enable 2-Factor Authentication on your Gmail account
2. Go to: Google Account → Security → 2-Step Verification → App passwords
3. Select app: "Mail" and device: "Other (Custom name)"
4. Enter name: "Leave Management System"
5. Copy the generated 16-character password
6. Use this password for `EMAIL_PASS` (NOT your regular Gmail password)

#### JWT Secret Key Generation:
```bash
# Generate a secure secret key
python -c "import secrets; print(secrets.token_hex(32))"
```

### 4. Run Development Server
```bash
uvicorn app.main:app --reload
```

The API will be available at: `http://localhost:8000`
Interactive API docs: `http://localhost:8000/docs`

## Production Deployment (Heroku)

### 1. Create Heroku App
```bash
heroku create your-app-name-api
```

### 2. Set Environment Variables
```bash
heroku config:set MONGODB_URI="mongodb+srv://username:password@cluster.mongodb.net/leaveapproval?retryWrites=true&w=majority"
heroku config:set SECRET_KEY="your-secure-secret-key"
heroku config:set EMAIL_USER="your-email@gmail.com"
heroku config:set EMAIL_PASS="your-gmail-app-password"
heroku config:set BACKEND_URL="https://your-app-name-api.herokuapp.com"
heroku config:set FRONTEND_URL="https://your-frontend-domain.com"
```

### 3. Deploy
```bash
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

## API Endpoints

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /auth/me` - Get current user info

### Leave Management
- `POST /leave/submit` - Submit leave request
- `GET /leave/my-requests` - Get user's leave requests
- `GET /leave/pending-approvals` - Get pending approvals (managers only)
- `POST /leave/{id}/approve` - Approve leave request
- `POST /leave/{id}/reject` - Reject leave request

### Email Integration
- `POST /leave/approve-with-token` - Approve via email token
- `GET /leave/reject-with-token` - Reject via email token

## Directory Structure
```
server/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── models/
│   │   ├── db.py           # Database connection and collections
│   │   └── schemas.py      # Pydantic models
│   ├── routes/
│   │   ├── auth.py         # Authentication endpoints
│   │   └── leave.py        # Leave management endpoints
│   └── utils/
│       ├── auth.py         # Authentication utilities
│       ├── email.py        # Email sending utilities
│       ├── tokens.py       # Token generation/verification
│       └── templates/      # Email templates
├── .env.example            # Environment variables template
├── .gitignore             # Git ignore file
├── requirements.txt       # Python dependencies
├── Procfile              # Heroku deployment config
└── README.md             # This file
```

## Troubleshooting

### Common Issues

**1. MongoDB Connection Error:**
```
pymongo.errors.ServerSelectionTimeoutError
```
- Check if MongoDB URI is correct
- Verify network access is allowed in MongoDB Atlas
- Ensure username/password are correct in connection string

**2. Email Not Sending:**
```
SMTPAuthenticationError: (535, '5.7.8 Username and Password not accepted')
```
- Verify you're using Gmail App Password, not regular password
- Ensure 2-Factor Authentication is enabled
- Check EMAIL_USER and EMAIL_PASS are correct

**3. JWT Token Error:**
```
JWTError: Invalid token
```
- Verify SECRET_KEY is set and consistent
- Check if token has expired
- Ensure token format is correct

**4. Import Errors:**
```
ModuleNotFoundError: No module named 'app'
```
- Run `pip install -r requirements.txt`
- Ensure you're in the server directory
- Check Python path configuration

### Development Tips

1. **View Logs:**
   ```bash
   # Local development
   uvicorn app.main:app --reload --log-level debug
   
   # Heroku production
   heroku logs --tail -a your-app-name
   ```

2. **Test Email Configuration:**
   ```bash
   # Use the test email endpoint
   curl -X POST "http://localhost:8000/auth/test-email" \
        -H "Authorization: Bearer YOUR_JWT_TOKEN"
   ```

3. **Database Inspection:**
   - Use MongoDB Compass or Atlas web interface
   - Check collections: `users`, `leaves`, `tokens`

## License
MIT
