#!/usr/bin/env python3
"""
Update chatbot with real TrueLearn Academy data
"""

import json
import re

def clean_html_tags(text):
    """Remove HTML tags from text"""
    if not text:
        return ""
    # Remove HTML tags
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text).strip()

def extract_clean_courses(raw_courses):
    """Extract clean course names from raw data"""
    clean_courses = []
    
    # Real courses from the website
    real_courses = [
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
    ]
    
    return real_courses

def clean_contact_info(raw_contact):
    """Clean contact information"""
    return {
        "email": "truelearnacademyblr@gmail.com",
        "phone": "+91 8333803232",
        "address": "DS complex, 14/3, Bommanahalli bus stop service road, beside VIDA showroom, Bommanahalli, Bangalore, Karnataka, 560068"
    }

def create_updated_chatbot_data():
    """Create updated chatbot data with real information"""
    
    chatbot_data = {
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
        },
        "about": "Industry-Aligned Training in WordPress, HTML/CSS, ServiceNow, Salesforce, SAP & Testing. We provide comprehensive training programs designed to meet industry standards and help students build successful careers in technology.",
        "social_links": {
            "facebook": "#",
            "twitter": "#", 
            "instagram": "#",
            "youtube": "https://www.youtube.com/watch?v=YLN1Argi7ik",
            "linkedin": "#"
        }
    }
    
    return chatbot_data

def update_app_py():
    """Update app.py with real data"""
    
    # Read current app.py
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create new ACADEMY_INFO
    chatbot_data = create_updated_chatbot_data()
    
    new_academy_info = f'''# Academy knowledge base
ACADEMY_INFO = {{
    "name": "{chatbot_data['name']}",
    "description": "{chatbot_data['description']}",
    "courses": {json.dumps(chatbot_data['courses'], indent=8)},
    "features": {json.dumps(chatbot_data['features'], indent=8)},
    "contact": {{
        "email": "{chatbot_data['contact']['email']}",
        "phone": "{chatbot_data['contact']['phone']}",
        "address": "{chatbot_data['contact']['address']}",
        "hours": "{chatbot_data['contact']['hours']}"
    }}
}}'''
    
    # Create new fallback responses
    new_fallback_responses = f'''# Enhanced fallback responses for when API is not available
FALLBACK_RESPONSES = {{
    "courses": "We offer: {', '.join(chatbot_data['courses'][:6])} and more. All courses include hands-on projects and industry-aligned training.",
    
    "pricing": "Course pricing varies. Contact us at {chatbot_data['contact']['phone']} for specific pricing and payment plans.",
    
    "enrollment": "Simple process: choose course, register, pay. We offer flexible payments and job placement assistance.",
    
    "contact": f"📧 {chatbot_data['contact']['email']} | 📞 {chatbot_data['contact']['phone']} | 🕒 {chatbot_data['contact']['hours']}",
    
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
    
    "schedule": "Flexible scheduling: {chatbot_data['contact']['hours']}. Weekend and weekday classes available.",
    
    "support": "24/7 support with dedicated mentors and industry experts.",
    
    "default": "Hi! I can help with courses, pricing, enrollment, and more. What do you need?"
}}'''
    
    # Replace the old ACADEMY_INFO and FALLBACK_RESPONSES
    content = re.sub(r'# Academy knowledge base\nACADEMY_INFO = \{.*?\}', new_academy_info, content, flags=re.DOTALL)
    content = re.sub(r'# Enhanced fallback responses for when API is not available\nFALLBACK_RESPONSES = \{.*?\}', new_fallback_responses, content, flags=re.DOTALL)
    
    # Write updated content
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Updated app.py with real TrueLearn Academy data!")

def main():
    """Main function"""
    print("🔄 Updating chatbot with real TrueLearn Academy data...")
    
    # Create updated data
    chatbot_data = create_updated_chatbot_data()
    
    # Save clean data
    with open('truelearn_real_data.json', 'w', encoding='utf-8') as f:
        json.dump(chatbot_data, f, indent=2, ensure_ascii=False)
    
    # Update app.py
    update_app_py()
    
    print("\n📊 Real Data Summary:")
    print("=" * 50)
    print(f"Name: {chatbot_data['name']}")
    print(f"Description: {chatbot_data['description'][:100]}...")
    print(f"Real Courses: {len(chatbot_data['courses'])}")
    print("Courses:")
    for course in chatbot_data['courses']:
        print(f"  - {course}")
    print(f"Contact: {chatbot_data['contact']['email']} | {chatbot_data['contact']['phone']}")
    print(f"Address: {chatbot_data['contact']['address']}")
    print(f"Hours: {chatbot_data['contact']['hours']}")
    
    print("\n🎉 Chatbot updated with real TrueLearn Academy data!")

if __name__ == "__main__":
    main() 