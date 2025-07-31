@echo off
echo ========================================
echo TrueLearn Academy Chatbot - Deployment
echo ========================================
echo.

echo Checking Git installation...
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git is not installed!
    echo Please install Git from: https://git-scm.com/download/win
    echo Then restart this script.
    pause
    exit /b 1
)

echo ✅ Git is installed
echo.

echo Current Git status:
git status
echo.

echo Do you want to:
echo 1. Initialize Git repository and make first commit
echo 2. Push to GitHub (requires GitHub repository URL)
echo 3. Just show deployment instructions
echo.

set /p choice="Enter your choice (1-3): "

if "%choice%"=="1" (
    echo.
    echo Initializing Git repository...
    git init
    git add .
    git commit -m "Initial commit: TrueLearn Academy Chatbot with real data"
    echo ✅ Repository initialized and files committed!
    echo.
    echo Next steps:
    echo 1. Create a repository on GitHub
    echo 2. Run this script again and choose option 2
    echo 3. Follow the deployment guide in DEPLOYMENT.md
)

if "%choice%"=="2" (
    echo.
    set /p repo_url="Enter your GitHub repository URL: "
    git remote add origin %repo_url%
    git branch -M main
    git push -u origin main
    echo ✅ Code pushed to GitHub!
    echo.
    echo Next steps:
    echo 1. Go to https://dashboard.render.com/
    echo 2. Create a new Web Service
    echo 3. Connect your GitHub repository
    echo 4. Add your GEMINI_API_KEY as environment variable
)

if "%choice%"=="3" (
    echo.
    echo 📖 Deployment Instructions:
    echo.
    echo 1. Install Git: https://git-scm.com/download/win
    echo 2. Create GitHub account: https://github.com/
    echo 3. Create Render account: https://render.com/
    echo 4. Follow detailed instructions in DEPLOYMENT.md
    echo.
    echo Quick commands:
    echo git init
    echo git add .
    echo git commit -m "Initial commit"
    echo git remote add origin YOUR_REPO_URL
    echo git push -u origin main
)

echo.
echo Press any key to exit...
pause >nul 