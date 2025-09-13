# Remove your current .env file from git tracking and create a secure version

# STEP 1: Remove from git (run this in your server directory)
git rm --cached .env

# STEP 2: Change your MongoDB password:
# - Go to MongoDB Atlas
# - Database Access > Edit User
# - Change password for 'Sagars' user
# - Update connection string below

# STEP 3: Regenerate Gmail app password:
# - Go to Google Account Settings
# - Security > App passwords
# - Generate new password for "Leave Approval App"

# STEP 4: Create new .env with new credentials:
MONGODB_URI=mongodb+srv://Sagars:[NEW_PASSWORD]@sagar.k5ggw.mongodb.net/leaveapproval?retryWrites=true&w=majority
SECRET_KEY=[GENERATE_NEW_SECRET_KEY]
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=[CONSIDER_USING_DIFFERENT_EMAIL]
EMAIL_PASS=[NEW_APP_PASSWORD]

# URL Configuration for Deployment
BACKEND_URL=http://localhost:8000
FRONTEND_URL=http://localhost:5173

# STEP 5: Update Heroku config variables with new values:
# heroku config:set MONGODB_URI="[new_connection_string]"
# heroku config:set SECRET_KEY="[new_secret]"
# heroku config:set EMAIL_PASS="[new_app_password]"