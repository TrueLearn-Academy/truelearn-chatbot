# 🤖 TrueLearn Academy Chatbot

An AI-powered chatbot for TrueLearn Academy that provides course information, enrollment details, and student support using Google Gemini API.

## ✨ Features

- 🤖 **AI-Powered Responses**: Uses Google Gemini API for intelligent conversations
- 📚 **Course Information**: Real data from TrueLearn Academy
- 📱 **Responsive Design**: Works on desktop and mobile
- ⚡ **Fast & Lightweight**: Optimized for performance
- 🔄 **Fallback System**: Works even when API is unavailable
- 🎨 **Modern UI**: Beautiful, professional interface

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Google Gemini API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd academy-chatbot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

4. **Run the chatbot**
   ```bash
   python app.py
   ```

5. **Access the chatbot**
   Open your browser and go to: `http://localhost:5000`

## 📁 Project Structure

```
academy-chatbot/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Chatbot interface
├── static/
│   └── favicon.ico       # Website icon
├── Procfile              # Render deployment
├── runtime.txt           # Python version
├── render.yaml           # Render configuration
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## 🌐 Deployment

### Deploy to Render

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy on Render**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Create new Web Service
   - Connect your GitHub repository
   - Add environment variable: `GEMINI_API_KEY`
   - Deploy!

## 🎯 Chatbot Capabilities

The chatbot can help with:
- 📚 **Course Information**: WordPress, HTML/CSS, ServiceNow, Salesforce, SAP, Testing, AI/ML, Cybersecurity, Cloud Computing, Full Stack Development
- 💰 **Pricing**: Course costs and payment plans
- 📝 **Enrollment**: How to register and join courses
- 📞 **Contact**: Email, phone, address, and business hours
- 🎓 **Career Guidance**: Job placement and certification information

## 🔧 Configuration

### Customize Responses
Edit `app.py` to modify:
- Academy information
- Course details
- Contact information
- Fallback responses

### Customize UI
Edit `templates/index.html` to change:
- Colors and styling
- Layout and design
- Chat interface

## 📞 Support

For issues or questions:
- Check the logs in your deployment platform
- Verify your API key is valid
- Test the `/api/health` endpoint

---

**🎉 Your TrueLearn Academy chatbot is ready to help students!** 