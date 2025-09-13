# Heroku Deployment Guide

## Backend Deployment (Heroku)

### 1. Prepare for Heroku
```bash
# Install Heroku CLI and login
heroku login

# Create Heroku app
heroku create your-leave-approval-api

# Add Python buildpack
heroku buildpacks:set heroku/python
```

### 2. Set Environment Variables
```bash
# Database
heroku config:set MONGODB_URI="mongodb+srv://production_user:production_password@production-cluster.mongodb.net/leaveapproval?retryWrites=true&w=majority"

# Security
heroku config:set SECRET_KEY="your-production-secret-key"

# Email
heroku config:set EMAIL_HOST="smtp.gmail.com"
heroku config:set EMAIL_PORT="587"
heroku config:set EMAIL_USER="your-email@gmail.com"
heroku config:set EMAIL_PASS="your-app-password"

# URLs for Mixed Environment (Backend on Heroku, Frontend Local)
heroku config:set BACKEND_URL="https://your-app-name.herokuapp.com"
heroku config:set FRONTEND_URL="http://localhost:5173"
```

### 3. Create Procfile
Create a file named `Procfile` in the server directory:
```
web: uvicorn app.main:app --host=0.0.0.0 --port=${PORT:-8000}
```

### 4. Update requirements.txt
Make sure your requirements.txt includes:
```
fastapi
uvicorn[standard]
pymongo
python-dotenv
passlib[bcrypt]
bcrypt==4.0.1
email-validator
jinja2
httpx
python-jose
python-multipart
```

### 5. Deploy
```bash
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

## Frontend Deployment (Netlify/Vercel)

### 1. Update environment variables
Create `.env.production` in client directory:
```
VITE_API_BASE_URL=https://your-leave-approval-api.herokuapp.com
```

### 2. Build and deploy
```bash
npm run build
# Deploy dist folder to Netlify/Vercel
```

## Environment Variables Summary

### For Heroku (Backend):
- `MONGODB_URI` - Your MongoDB connection string
- `SECRET_KEY` - JWT secret key for production
- `EMAIL_HOST` - SMTP host (gmail: smtp.gmail.com)
- `EMAIL_PORT` - SMTP port (gmail: 587)
- `EMAIL_USER` - Your Gmail address
- `EMAIL_PASS` - Gmail App Password
- `BACKEND_URL` - Your Heroku backend URL (https://your-app.herokuapp.com)
- `FRONTEND_URL` - Your local frontend URL (http://localhost:5173)

### For Local Frontend (.env):
- `VITE_API_URL` - Points to your Heroku backend (https://your-app.herokuapp.com)

## Mixed Environment Setup (Backend on Heroku, Frontend Local)

This is perfect for development when you need HTTPS for AMP emails but want to develop frontend locally:

### ✅ **What Works:**
- **AMP Emails**: Submit to HTTPS Heroku backend ✅
- **Approval Forms**: Work directly in email with HTTPS ✅  
- **Rejection Redirect**: Opens local frontend dashboard ✅
- **API Calls**: Frontend calls Heroku backend via HTTPS ✅

### 🔧 **Configuration:**
```bash
# Heroku Backend Environment
BACKEND_URL=https://your-app.herokuapp.com
FRONTEND_URL=http://localhost:5173

# Local Frontend Environment (.env)
VITE_API_URL=https://your-app.herokuapp.com
```

### 📧 **Email Flow:**
1. **Email generated** with Heroku URLs
2. **Approve button** → submits to Heroku (HTTPS) ✅
3. **Reject button** → redirects to localhost:5173 ✅
4. **Dashboard** → calls Heroku API ✅

## Important Notes:

1. **HTTPS Requirement**: Only backend needs HTTPS for AMP emails
2. **CORS**: Already configured for localhost:5173 in your backend
3. **No SSL needed**: Frontend can run on HTTP localhost
4. **Gmail**: Use App Passwords for Gmail SMTP authentication

## Testing Mixed Environment:
1. Deploy backend to Heroku with correct environment variables
2. Run frontend locally: `npm run dev`
3. Submit leave request through local frontend
4. Check email has Heroku URLs for approval, localhost for rejection
5. Test both approval (in email) and rejection (redirect to localhost) flows
