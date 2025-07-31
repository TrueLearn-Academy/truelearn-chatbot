@echo off
echo ========================================
echo Creating WordPress Plugin Package
echo ========================================
echo.

echo Creating plugin directory structure...
if not exist "truelearn-chatbot-widget" mkdir "truelearn-chatbot-widget"
if not exist "truelearn-chatbot-widget\assets" mkdir "truelearn-chatbot-widget\assets"

echo Copying files...
copy "wordpress-integration\truelearn-chatbot-widget.php" "truelearn-chatbot-widget\"
copy "wordpress-integration\assets\chatbot-widget.css" "truelearn-chatbot-widget\assets\"
copy "wordpress-integration\assets\chatbot-widget.js" "truelearn-chatbot-widget\assets\"
copy "wordpress-integration\README.md" "truelearn-chatbot-widget\"
copy "wordpress-integration\install-guide.txt" "truelearn-chatbot-widget\"

echo.
echo ✅ WordPress plugin files created in 'truelearn-chatbot-widget' folder
echo.
echo 📋 Next steps:
echo 1. Edit 'truelearn-chatbot-widget\truelearn-chatbot-widget.php'
echo 2. Update the API URL on line 108 with your Render app URL
echo 3. Zip the 'truelearn-chatbot-widget' folder
echo 4. Upload to WordPress Admin → Plugins → Add New → Upload Plugin
echo.
echo Press any key to open the plugin folder...
pause >nul
start "" "truelearn-chatbot-widget" 