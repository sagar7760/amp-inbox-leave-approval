# Leave Management System

A complete full-stack web application for employee leave management with email-based approval workflow. Built with React (frontend) and FastAPI (backend).

## 🚀 Features

- **Employee Portal**: Submit leave requests, view status and history
- **Manager Dashboard**: Review and approve/reject leave requests  
- **Email Integration**: AMP email support for in-inbox approvals
- **Secure Authentication**: JWT-based auth with role management
- **Responsive Design**: Mobile-first UI with modern design
- **Real-time Updates**: Dashboard statistics and status tracking

## 🛠️ Technology Stack

### Frontend
- **React 19** - Modern React with hooks
- **Tailwind CSS** - Utility-first styling
- **Vite** - Fast development server
- **React Router** - Client-side routing

### Backend  
- **FastAPI** - High-performance Python API
- **MongoDB** - NoSQL database
- **JWT Authentication** - Secure token-based auth
- **AMP Email** - Interactive email templates

## 📋 Prerequisites

Before setting up this project, ensure you have:

- **Node.js 18+** and npm/yarn
- **Python 3.8+** and pip
- **MongoDB Atlas** account (or local MongoDB)
- **Gmail** account with App Password enabled

## ⚡ Quick Setup

### 1. Clone Backend Repository 
```bash
git clone https://github.com/sagar7760/amp-inbox-leave-approval.git
cd amp-inbox-leave-approval
```

### 2. Backend Setup

```bash
cd server

# Install Python dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
```

**Configure `.env` file:**
```env
# Database Configuration
MONGODB_URI=mongodb+srv://YOUR_USERNAME:YOUR_PASSWORD@YOUR_CLUSTER.mongodb.net/leaveapproval?retryWrites=true&w=majority

# Security
SECRET_KEY=your-secret-jwt-key-here

# Email Configuration (Gmail)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your-email@gmail.com
EMAIL_PASS=your-gmail-app-password

# URLs
BACKEND_URL=http://localhost:8000
FRONTEND_URL=http://localhost:5173
```

**Start backend server:**
```bash
uvicorn app.main:app --reload
```

### 3. Frontend Setup

```bash
cd ../client

# Install dependencies
npm install

# Configure environment
cp .env.example .env
```

**Configure `.env` file:**
```env
VITE_API_BASE_URL=http://localhost:8000
```

**Start frontend:**
```bash
npm run dev
```

## 🔧 Environment Variables Setup Guide

### MongoDB Atlas Setup
1. Create account at [MongoDB Atlas](https://www.mongodb.com/atlas)
2. Create a new cluster
3. Create database user with read/write access
4. Get connection string and update `MONGODB_URI`

### Gmail App Password Setup
1. Enable 2-Factor Authentication on your Gmail account
2. Go to Google Account Settings → Security → App passwords
3. Generate password for "Leave Management App"
4. Use this password for `EMAIL_PASS` (not your regular Gmail password)

### JWT Secret Key
Generate a secure secret key:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

## 🚀 Deployment

### Heroku Deployment

**Backend (FastAPI):**
```bash
cd server

# Login to Heroku
heroku login

# Create Heroku app
heroku create your-app-name-api

# Set environment variables
heroku config:set MONGODB_URI="your_mongodb_connection_string"
heroku config:set SECRET_KEY="your_jwt_secret"
heroku config:set EMAIL_USER="your_email@gmail.com"
heroku config:set EMAIL_PASS="your_gmail_app_password"
heroku config:set BACKEND_URL="https://your-app-name-api.herokuapp.com"
heroku config:set FRONTEND_URL="https://your-frontend-url.netlify.app"

# Deploy
git push heroku main
```

**Frontend (React):**
- Deploy to Netlify, Vercel, or similar
- Update `VITE_API_BASE_URL` to point to your Heroku backend URL

## 📁 Project Structure

```
leave-approval/
├── client/                 # React frontend
│   ├── src/
│   │   ├── pages/         # React pages/routes
│   │   ├── components/    # Reusable components
│   │   ├── services/      # API service layer
│   │   └── contexts/      # React context providers
│   ├── .env.example       # Environment template
│   └── package.json
│
├── server/                 # FastAPI backend  
│   ├── app/
│   │   ├── routes/        # API endpoints
│   │   ├── models/        # Database models
│   │   ├── utils/         # Utility functions
│   │   └── main.py        # FastAPI app entry
│   ├── .env.example       # Environment template
│   └── requirements.txt
│
└── README.md              # This file
```

## 🔐 Security Notes

- Never commit real `.env` files to version control
- Use strong, unique passwords for database and email
- Regularly rotate JWT secret keys
- Enable MongoDB IP whitelist in production
- Use HTTPS in production deployments

## 🐛 Troubleshooting

### Common Issues

**Backend won't start:**
- Check if MongoDB URI is correct
- Verify all required environment variables are set
- Ensure Python dependencies are installed

**Frontend can't connect to API:**
- Verify `VITE_API_BASE_URL` matches backend URL
- Check if backend server is running
- Ensure CORS is configured properly

**Email notifications not working:**
- Verify Gmail app password (not regular password)
- Check if 2FA is enabled on Gmail account
- Confirm EMAIL_USER and EMAIL_PASS are correct

## 📧 Support

For questions or issues:
1. Check the troubleshooting section above
2. Review environment variable setup
3. Create an issue on GitHub repository

## 📄 License

MIT License - See LICENSE file for details

---

## 🎯 Default Login Credentials (Development)

After running the project locally, you can create accounts through the registration page, or use the test data script if available.

**Manager Account Example:**
- Email: manager@company.com
- Password: (set during registration)
- Role: Manager (set `is_manager: true` in MongoDB)

**Employee Account Example:**  
- Email: employee@company.com
- Password: (set during registration)
- Role: Employee (default)