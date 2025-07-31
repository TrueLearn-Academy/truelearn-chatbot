# TrueLearn Academy Chatbot

An intelligent AI-powered chatbot for TrueLearn Academy, built with Flask and Google's Gemini API. This chatbot provides comprehensive support for students, helping them with course information, enrollment, pricing, and technical support.

## Features

- 🤖 **AI-Powered Responses**: Uses Google Gemini API for intelligent, contextual responses
- 📚 **Course Information**: Detailed information about available courses and learning paths
- 💰 **Pricing & Enrollment**: Help with course pricing and enrollment procedures
- 📞 **Technical Support**: Assistance with platform usage and technical issues
- 🏆 **Career Guidance**: Information about certificates and career opportunities
- 📱 **Responsive Design**: Beautiful, modern UI that works on all devices
- ⚡ **Real-time Chat**: Instant responses with typing indicators
- 🎯 **Quick Replies**: Pre-defined quick response buttons for common queries

## Available Courses

- Web Development
- Data Science
- Digital Marketing
- Business Management
- Personal Development
- Programming Fundamentals
- AI and Machine Learning
- Cybersecurity

## Technology Stack

- **Backend**: Flask (Python)
- **AI**: Google Gemini API
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Custom CSS with modern gradients and animations
- **Icons**: Font Awesome

## Setup Instructions

### Prerequisites

- Python 3.7 or higher
- Google Gemini API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd academy-chatbot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Copy the example environment file
   cp env_example.txt .env
   
   # Edit .env and add your Gemini API key
   GEMINI_API_KEY=your_actual_api_key_here
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the chatbot**
   Open your browser and go to `http://localhost:5000`

### Getting a Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated API key
5. Add it to your `.env` file

## Project Structure

```
academy-chatbot/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── env_example.txt        # Environment variables template
├── README.md             # This file
└── templates/
    └── index.html        # Chatbot interface
```

## API Endpoints

- `GET /` - Main chatbot interface
- `POST /api/chat` - Send messages to the chatbot
- `GET /api/courses` - Get available courses
- `GET /api/contact` - Get contact information

## Customization

### Updating Academy Information

Edit the `ACADEMY_INFO` dictionary in `app.py` to customize:

- Course offerings
- Contact information
- Features and benefits
- Academy description

### Styling

The chatbot interface can be customized by modifying the CSS in `templates/index.html`. The design uses:

- Modern gradient backgrounds
- Smooth animations and transitions
- Responsive design principles
- Professional color scheme

### System Prompt

The AI's behavior can be customized by modifying the `create_system_prompt()` function in `app.py`. This controls:

- How the AI responds to questions
- What information it provides
- The tone and style of responses

## Deployment

### Local Development
```bash
python app.py
```

### Production Deployment

For production deployment, consider using:

- **WSGI Server**: Gunicorn or uWSGI
- **Reverse Proxy**: Nginx
- **Process Manager**: PM2 or Supervisor
- **Environment**: Set `FLASK_ENV=production`

Example with Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Security Considerations

- Keep your API key secure and never commit it to version control
- Use HTTPS in production
- Implement rate limiting for API endpoints
- Consider adding user authentication for sensitive operations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support or questions about the chatbot, please contact:
- Email: info@truelearnacademy.com
- Phone: +1-555-ACADEMY

## Future Enhancements

- [ ] User authentication and session management
- [ ] Chat history and conversation persistence
- [ ] File upload support for course materials
- [ ] Integration with learning management system
- [ ] Multi-language support
- [ ] Voice chat capabilities
- [ ] Advanced analytics and reporting 