from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Try different model names in order of preference
def get_gemini_model():
    model_names = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-2.0-flash', 'gemini-2.5-flash']
    
    for model_name in model_names:
        try:
            model = genai.GenerativeModel(model_name)
            # Test the model with a simple prompt
            response = model.generate_content("Hello")
            print(f"Successfully connected to {model_name}")
            return model
        except Exception as e:
            print(f"Failed to connect to {model_name}: {str(e)}")
            continue
    
    # If all models fail, try to list available models
    try:
        print("Attempting to list available models...")
        models = genai.list_models()
        available_models = []
        for m in models:
            if 'generateContent' in m.supported_generation_methods:
                available_models.append(m.name)
                print(f"Available model: {m.name}")
        
        if available_models:
            # Try the first available model
            model = genai.GenerativeModel(available_models[0])
            response = model.generate_content("Hello")
            print(f"Successfully connected to {available_models[0]}")
            return model
    except Exception as e:
        print(f"Failed to list models: {str(e)}")
    
    print("Warning: Could not connect to any Gemini model. Using fallback responses.")
    return None

model = get_gemini_model()

# Academy knowledge base
ACADEMY_INFO = {
    "name": "TrueLearn Academy",
    "description": "At TrueLearn Academy, we empower individuals with the skills they need to thrive in today's fast-paced tech-driven world. As a leading provider of industry-focused technology courses, we specialize in delivering hands-on training across areas like Software Development, Data Science, AI & ML, Cybersecurity, Cloud Computing, Full Stack Development, and more.",
    "courses": [
        "WordPress Development",
        "HTML/CSS Development",
        "ServiceNow Training",
        "Salesforce Training",
        "SAP Training",
        "Software Testing",
        "Software Development",
        "Data Science",
        "AI & Machine Learning",
        "Cybersecurity",
        "Cloud Computing",
        "Full Stack Development"
],
    "features": [
        "Industry-aligned training",
        "Hands-on practical experience",
        "Expert instructors",
        "Flexible scheduling",
        "Certificate upon completion",
        "Job placement assistance",
        "Real-world projects",
        "24/7 support"
],
    "contact": {
        "email": "truelearnacademyblr@gmail.com",
        "phone": "+91 8333803232",
        "address": "DS complex, 14/3, Bommanahalli bus stop service road, beside VIDA showroom, Bommanahalli, Bangalore, Karnataka, 560068",
        "hours": "Mon to Saturday 9AM to 7PM"
    }
}

# Enhanced fallback responses for when API is not available
FALLBACK_RESPONSES = {
    "courses": "We offer:\n• WordPress Development\n• HTML/CSS Development\n• ServiceNow Training\n• Salesforce Training\n• SAP Training\n• Software Testing\n• Software Development\n• Data Science\n• AI & Machine Learning\n• Cybersecurity\n• Cloud Computing\n• Full Stack Development\n\nAll courses include hands-on projects and industry-aligned training.",
    
    "pricing": "Course pricing varies. Contact us at +91 8333803232 for specific pricing and payment plans.",
    
    "enrollment": "Simple process: choose course, register, pay. We offer flexible payments and job placement assistance.",
    
    "contact": f"📧 {ACADEMY_INFO['contact']['email']}\n📞 {ACADEMY_INFO['contact']['phone']}\n🕒 {ACADEMY_INFO['contact']['hours']}\n📍 {ACADEMY_INFO['contact']['address']}",
    
    "wordpress": "WordPress Development: Learn to build professional websites. Hands-on training with real projects.",
    
    "html_css": "HTML/CSS Development: Master frontend development. Create responsive and modern websites.",
    
    "servicenow": "ServiceNow Training: Learn ServiceNow platform. Industry-recognized certification preparation.",
    
    "salesforce": "Salesforce Training: Master Salesforce CRM. Prepare for Salesforce certifications.",
    
    "sap": "SAP Training: Learn SAP modules. Industry-focused training for SAP careers.",
    
    "testing": "Software Testing: Learn manual and automated testing. ISTQB certification preparation.",
    
    "ai_ml": "AI & ML: Python, TensorFlow, neural networks, computer vision. Industry-aligned curriculum.",
    
    "cybersecurity": "Cybersecurity: Ethical hacking, network security, cryptography. Hands-on lab training.",
    
    "cloud": "Cloud Computing: AWS, Azure, Google Cloud. Learn cloud infrastructure and services.",
    
    "fullstack": "Full Stack Development: Frontend, backend, databases. End-to-end web development.",
    
    "certificate": "All courses provide industry-recognized certificates upon completion.",
    
    "career": "We provide career guidance, job placement assistance, and industry networking.",
    
    "schedule": "Flexible scheduling: Mon to Saturday 9AM to 7PM. Weekend and weekday classes available.",
    
    "support": "24/7 support with dedicated mentors and industry experts.",
    
    "default": "Hi! I can help with:\n• Course information\n• Pricing details\n• Enrollment process\n• Contact information\n\nWhat would you like to know?"
}

def get_fallback_response(user_message):
    """Get appropriate fallback response based on user message"""
    message_lower = user_message.lower()
    
    # More comprehensive keyword matching with better context understanding
    if any(word in message_lower for word in ['course', 'offer', 'available', 'what', 'program', 'learn', 'study']):
        return FALLBACK_RESPONSES['courses']
    elif any(word in message_lower for word in ['price', 'cost', 'fee', 'how much', 'payment', 'money', 'expensive', 'cheap']):
        return FALLBACK_RESPONSES['pricing']
    elif any(word in message_lower for word in ['enroll', 'register', 'sign up', 'join', 'apply', 'start', 'begin']):
        return FALLBACK_RESPONSES['enrollment']
    elif any(word in message_lower for word in ['contact', 'email', 'phone', 'address', 'reach', 'talk', 'speak']):
        return FALLBACK_RESPONSES['contact']
    elif any(word in message_lower for word in ['wordpress', 'wp', 'cms']):
        return FALLBACK_RESPONSES['wordpress']
    elif any(word in message_lower for word in ['html', 'css', 'frontend', 'web', 'website']):
        return FALLBACK_RESPONSES['html_css']
    elif any(word in message_lower for word in ['servicenow', 'service now', 'itil']):
        return FALLBACK_RESPONSES['servicenow']
    elif any(word in message_lower for word in ['salesforce', 'crm', 'sf']):
        return FALLBACK_RESPONSES['salesforce']
    elif any(word in message_lower for word in ['sap', 'erp', 'enterprise']):
        return FALLBACK_RESPONSES['sap']
    elif any(word in message_lower for word in ['testing', 'qa', 'quality assurance', 'manual', 'automation']):
        return FALLBACK_RESPONSES['testing']
    elif any(word in message_lower for word in ['ai', 'artificial intelligence', 'machine learning', 'ml', 'neural', 'tensorflow']):
        return FALLBACK_RESPONSES['ai_ml']
    elif any(word in message_lower for word in ['security', 'cyber', 'hacking', 'ethical', 'protect', 'safe']):
        return FALLBACK_RESPONSES['cybersecurity']
    elif any(word in message_lower for word in ['cloud', 'aws', 'azure', 'google cloud', 'gcp']):
        return FALLBACK_RESPONSES['cloud']
    elif any(word in message_lower for word in ['full stack', 'fullstack', 'backend', 'database', 'full stack development']):
        return FALLBACK_RESPONSES['fullstack']
    elif any(word in message_lower for word in ['certificate', 'certification', 'diploma', 'credential', 'proof']):
        return FALLBACK_RESPONSES['certificate']
    elif any(word in message_lower for word in ['career', 'job', 'employment', 'work', 'salary', 'position']):
        return FALLBACK_RESPONSES['career']
    elif any(word in message_lower for word in ['schedule', 'time', 'duration', 'when', 'how long', 'flexible']):
        return FALLBACK_RESPONSES['schedule']
    elif any(word in message_lower for word in ['support', 'help', 'assistance', 'mentor', 'tutor', 'guide']):
        return FALLBACK_RESPONSES['support']
    elif any(word in message_lower for word in ['hello', 'hi', 'hey', 'good morning', 'good afternoon']):
        return "Hi! Welcome to TrueLearn Academy. How can I help you today?"
    elif any(word in message_lower for word in ['thank', 'thanks', 'appreciate']):
        return "You're welcome! Anything else I can help with?"
    elif any(word in message_lower for word in ['bye', 'goodbye', 'see you', 'later']):
        return "Thanks for visiting! Come back anytime. Good luck! 🎓"
    else:
        return FALLBACK_RESPONSES['default']

def create_system_prompt():
    """Create a comprehensive system prompt for the academy chatbot"""
    return f"""
    You are an AI assistant for {ACADEMY_INFO['name']}. Keep responses SHORT, CRISP, and CLEAR.
    
    Academy Info:
    - Courses: {', '.join(ACADEMY_INFO['courses'])}
    - Contact: {ACADEMY_INFO['contact']['email']} | {ACADEMY_INFO['contact']['phone']}
    
    Guidelines:
    - Keep responses under 2-3 sentences
    - Be direct and helpful
    - Use bullet points (•) when listing multiple items
    - Format lists properly with line breaks
    - Be friendly but concise
    - If unsure, suggest contacting the academy
    
    When listing courses, use this format:
    We offer:
    • Course 1
    • Course 2
    • Course 3
    
    Help with: courses, pricing, enrollment, contact info, and general questions.
    """

@app.route('/')
def home():
    """Render the main chatbot interface"""
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    """Serve favicon"""
    return app.send_static_file('favicon.ico')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Check if API key is configured
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key or api_key == 'your_gemini_api_key_here':
            return jsonify({
                'error': 'Gemini API key not configured. Please set GEMINI_API_KEY in your .env file.',
                'status': 'error'
            }), 500
        
        # Try to use Gemini API if available
        if model:
            try:
                # Create conversation with system prompt
                system_prompt = create_system_prompt()
                
                # Generate response using Gemini
                response = model.generate_content([
                    system_prompt,
                    user_message
                ])
                
                return jsonify({
                    'response': response.text,
                    'status': 'success'
                })
            except Exception as api_error:
                print(f"API Error: {str(api_error)}")
                # Fall through to fallback response
        
        # Use fallback response if API is not available or fails
        fallback_response = get_fallback_response(user_message)
        return jsonify({
            'response': fallback_response,
            'status': 'success',
            'note': 'Using fallback response (API unavailable)'
        })
        
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return jsonify({
            'error': f'Server error: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/api/courses')
def get_courses():
    """Get available courses"""
    return jsonify({
        'courses': ACADEMY_INFO['courses'],
        'features': ACADEMY_INFO['features']
    })

@app.route('/api/contact')
def get_contact():
    """Get contact information"""
    return jsonify(ACADEMY_INFO['contact'])

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    api_key = os.getenv('GEMINI_API_KEY')
    
    # Test model connection
    model_status = "unknown"
    if model:
        try:
            # Try a simple test
            test_response = model.generate_content("Test")
            model_status = "connected"
        except Exception as e:
            model_status = f"error: {str(e)}"
    else:
        model_status = "not available (using fallback)"
    
    return jsonify({
        'status': 'healthy',
        'api_key_configured': bool(api_key and api_key != 'your_gemini_api_key_here'),
        'academy_name': ACADEMY_INFO['name'],
        'model_status': model_status
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port) 