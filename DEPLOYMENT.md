# 🚀 TrueLearn Academy Chatbot - Deployment Guide

## 📋 Prerequisites

1. **Git Installation**: Download and install Git from https://git-scm.com/
2. **GitHub Account**: Create a free account at https://github.com/
3. **Render Account**: Sign up at https://render.com/

## 🔧 Step 1: Install Git

### Windows:
1. Download Git from https://git-scm.com/download/win
2. Run the installer with default settings
3. Restart your terminal/PowerShell

### Verify Installation:
```bash
git --version
```

## 📁 Step 2: Initialize Git Repository

```bash
# Initialize Git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: TrueLearn Academy Chatbot"

# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/truelearn-chatbot.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## 🌐 Step 3: Deploy to Render

### Option A: Connect GitHub Repository (Recommended)

1. **Go to Render Dashboard**: https://dashboard.render.com/
2. **Click "New +"** → **"Web Service"**
3. **Connect your GitHub repository**
4. **Configure the service**:
   - **Name**: `truelearn-academy-chatbot`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`
   - **Plan**: Free

5. **Add Environment Variables**:
   - **Key**: `GEMINI_API_KEY`
   - **Value**: Your actual Gemini API key

6. **Click "Create Web Service"**

### Option B: Manual Upload

1. **Create a new Web Service** on Render
2. **Upload your code** as a ZIP file
3. **Configure the same settings** as above

## 🔑 Step 4: Environment Variables

In Render dashboard, add these environment variables:

| Key | Value | Description |
|-----|-------|-------------|
| `GEMINI_API_KEY` | `your_actual_api_key` | Your Google Gemini API key |
| `FLASK_ENV` | `production` | Production environment |
| `FLASK_DEBUG` | `False` | Disable debug mode |

## 🌍 Step 5: Access Your Chatbot

Once deployed, your chatbot will be available at:
```
https://your-app-name.onrender.com
```

## 🔄 Step 6: Updates

To update your chatbot:

```bash
# Make your changes
git add .
git commit -m "Update chatbot features"
git push origin main
```

Render will automatically redeploy your application.

## 🛠️ Troubleshooting

### Common Issues:

1. **Build Fails**: Check that all dependencies are in `requirements.txt`
2. **API Key Error**: Verify `GEMINI_API_KEY` is set in Render environment variables
3. **Port Issues**: Ensure `gunicorn` is in requirements.txt and Procfile is correct

### Logs:
- Check Render dashboard → Your service → Logs
- Look for error messages in the build or runtime logs

## 📞 Support

If you encounter issues:
1. Check Render documentation: https://render.com/docs
2. Verify your API key is working locally first
3. Check the logs in Render dashboard

---

**🎉 Your TrueLearn Academy Chatbot is now live and ready to help students!** 