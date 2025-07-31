@echo off
echo TrueLearn Academy Chatbot Setup
echo ================================

echo.
echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

echo Python is installed!

echo.
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Checking for .env file...
if not exist .env (
    echo Creating .env file from template...
    copy env_example.txt .env
    echo.
    echo IMPORTANT: Please edit .env file and add your Gemini API key
    echo 1. Open .env file in a text editor
    echo 2. Replace 'your_gemini_api_key_here' with your actual API key
    echo 3. Save the file
    echo.
    echo To get a Gemini API key:
    echo 1. Go to https://makersuite.google.com/app/apikey
    echo 2. Sign in with your Google account
    echo 3. Click "Create API Key"
    echo 4. Copy the generated key
    echo.
    pause
) else (
    echo .env file found!
)

echo.
echo Starting the chatbot...
echo The chatbot will be available at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
python app.py

pause 