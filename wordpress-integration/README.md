# 🎯 TrueLearn Academy Chatbot Widget for WordPress

A beautiful, responsive chat widget that integrates your AI-powered chatbot directly into your WordPress website.

## ✨ Features

- 🎨 **Modern Design**: Beautiful gradient design with smooth animations
- 📱 **Mobile Responsive**: Works perfectly on all devices
- 🤖 **AI-Powered**: Connects to your Flask chatbot API
- ⚡ **Fast & Lightweight**: Optimized for performance
- 🔒 **Secure**: WordPress nonce verification
- 🎯 **Quick Replies**: Pre-defined response buttons
- 💬 **Real-time Chat**: Live typing indicators and smooth interactions

## 📦 Installation

### Method 1: Manual Installation

1. **Download the Plugin Files**
   - Copy the `wordpress-integration` folder to your computer
   - Rename it to `truelearn-chatbot-widget`

2. **Upload to WordPress**
   - Go to your WordPress admin panel
   - Navigate to **Plugins** → **Add New** → **Upload Plugin**
   - Upload the `truelearn-chatbot-widget` folder as a ZIP file
   - Click **Install Now** and then **Activate**

3. **Configure API URL**
   - Edit the file `truelearn-chatbot-widget.php`
   - Find line 108: `$api_url = 'https://your-app-name.onrender.com/api/chat';`
   - Replace `your-app-name` with your actual Render app name

### Method 2: Direct File Upload

1. **Create Plugin Directory**
   ```bash
   wp-content/plugins/truelearn-chatbot-widget/
   ```

2. **Upload Files**
   - Upload `truelearn-chatbot-widget.php` to the plugin directory
   - Create `assets/` folder and upload:
     - `chatbot-widget.css`
     - `chatbot-widget.js`

3. **Activate Plugin**
   - Go to WordPress admin → Plugins
   - Find "TrueLearn Academy Chatbot Widget"
   - Click **Activate**

## ⚙️ Configuration

### 1. Update API URL

Edit `truelearn-chatbot-widget.php` and update the API URL:

```php
// Line 108 - Replace with your actual Render URL
$api_url = 'https://your-app-name.onrender.com/api/chat';
```

### 2. Customize Appearance (Optional)

Edit `assets/chatbot-widget.css` to customize:

- **Colors**: Change the gradient colors
- **Position**: Modify widget position
- **Size**: Adjust chat window dimensions
- **Fonts**: Change typography

### 3. Customize Messages (Optional)

Edit `truelearn-chatbot-widget.php` to customize:

- Welcome message
- Quick reply buttons
- Error messages

## 🎨 Customization Examples

### Change Colors
```css
/* In chatbot-widget.css */
.truelearn-chat-icon {
    background: linear-gradient(135deg, #your-color-1 0%, #your-color-2 100%);
}
```

### Change Position
```css
/* Move to bottom-left */
.truelearn-chat-widget {
    bottom: 20px;
    left: 20px;
    right: auto;
}
```

### Change Size
```css
/* Make chat window larger */
.truelearn-chat-window {
    width: 400px;
    height: 600px;
}
```

## 🔧 Troubleshooting

### Chat Widget Not Appearing
1. Check if plugin is activated
2. Clear browser cache
3. Check browser console for JavaScript errors
4. Verify jQuery is loaded

### API Connection Issues
1. Verify your Render app is running
2. Check the API URL in the plugin file
3. Test the API endpoint directly
4. Check WordPress error logs

### Styling Issues
1. Clear browser cache
2. Check if CSS file is loading
3. Verify Font Awesome is accessible
4. Check for theme conflicts

## 📱 Mobile Optimization

The widget is fully responsive and includes:

- Touch-friendly buttons
- Mobile-optimized layout
- Proper viewport handling
- Swipe gestures support

## 🔒 Security Features

- WordPress nonce verification
- Input sanitization
- AJAX security checks
- XSS protection

## 🚀 Performance Tips

1. **Enable Caching**: Use a caching plugin
2. **Optimize Images**: Compress any custom images
3. **Minify CSS/JS**: Use optimization plugins
4. **CDN**: Serve assets from CDN

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Verify your Flask API is working
3. Test with a simple message first
4. Check browser developer tools

## 🎯 Quick Test

After installation:

1. Visit your WordPress site
2. Look for the chat icon in the bottom-right corner
3. Click the icon to open the chat
4. Try sending a test message
5. Verify you get a response from your AI

## 📋 File Structure

```
truelearn-chatbot-widget/
├── truelearn-chatbot-widget.php    # Main plugin file
├── assets/
│   ├── chatbot-widget.css         # Styles
│   └── chatbot-widget.js          # JavaScript
└── README.md                      # This file
```

## 🔄 Updates

To update the widget:

1. Deactivate the plugin
2. Upload new files
3. Reactivate the plugin
4. Clear any caches

---

**🎉 Your TrueLearn Academy chatbot is now integrated into your WordPress website!** 