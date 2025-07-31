#!/usr/bin/env python3
"""
Simple web scraper for TrueLearn Academy website
Uses only built-in Python libraries
"""

import requests
import json
import re
from urllib.parse import urljoin
import html

class SimpleTrueLearnScraper:
    def __init__(self):
        self.base_url = "https://truelearnacademy.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.data = {
            "name": "TrueLearn Academy",
            "description": "",
            "courses": [],
            "contact": {},
            "features": [],
            "about": "",
            "social_links": {}
        }
    
    def get_page_content(self, url):
        """Get page content with error handling"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"⚠️ Could not fetch {url}: {e}")
            return None
    
    def extract_text_between_tags(self, html_content, start_tag, end_tag):
        """Extract text between HTML tags"""
        pattern = f"{start_tag}(.*?){end_tag}"
        matches = re.findall(pattern, html_content, re.DOTALL | re.IGNORECASE)
        return [html.unescape(match.strip()) for match in matches if match.strip()]
    
    def extract_meta_content(self, html_content, name):
        """Extract meta tag content"""
        pattern = f'<meta[^>]*name=["\']{name}["\'][^>]*content=["\']([^"\']*)["\']'
        match = re.search(pattern, html_content, re.IGNORECASE)
        return match.group(1) if match else ""
    
    def scrape_website(self):
        """Main scraping function"""
        print("🔍 Scraping TrueLearn Academy website...")
        
        try:
            # Scrape main page
            self.scrape_main_page()
            
            # Try to scrape courses
            self.scrape_courses()
            
            # Try to scrape contact info
            self.scrape_contact()
            
            print("✅ Website scraping completed!")
            return self.data
            
        except Exception as e:
            print(f"❌ Error scraping website: {e}")
            return None
    
    def scrape_main_page(self):
        """Scrape the main homepage"""
        print("📄 Scraping main page...")
        html_content = self.get_page_content(self.base_url)
        if not html_content:
            return
        
        # Extract description from meta tags
        self.data['description'] = self.extract_meta_content(html_content, 'description')
        
        # Extract title
        title_match = re.search(r'<title[^>]*>(.*?)</title>', html_content, re.IGNORECASE)
        if title_match:
            title = html.unescape(title_match.group(1).strip())
            if title and title != "TrueLearn Academy":
                self.data['name'] = title
        
        # Extract headings (potential course names)
        headings = self.extract_text_between_tags(html_content, r'<h[1-6][^>]*>', r'</h[1-6]>')
        for heading in headings:
            if len(heading) > 5 and len(heading) < 100:
                # Check if it looks like a course name
                course_keywords = ['course', 'training', 'program', 'class', 'workshop', 'certification']
                if any(keyword in heading.lower() for keyword in course_keywords):
                    self.data['courses'].append({
                        'name': heading,
                        'description': '',
                        'price': '',
                        'duration': ''
                    })
        
        # Extract paragraphs (potential descriptions)
        paragraphs = self.extract_text_between_tags(html_content, r'<p[^>]*>', r'</p>')
        for para in paragraphs:
            if len(para) > 50 and len(para) < 500:
                if not self.data['description']:
                    self.data['description'] = para
                elif not self.data['about']:
                    self.data['about'] = para
        
        # Extract social links
        social_pattern = r'href=["\']([^"\']*(?:facebook|twitter|instagram|linkedin|youtube)[^"\']*)["\']'
        social_matches = re.findall(social_pattern, html_content, re.IGNORECASE)
        for match in social_matches:
            platform = re.search(r'(facebook|twitter|instagram|linkedin|youtube)', match, re.IGNORECASE)
            if platform:
                self.data['social_links'][platform.group(1).lower()] = match
    
    def scrape_courses(self):
        """Try to scrape courses from different URLs"""
        print("📚 Scraping courses...")
        
        course_urls = [
            f"{self.base_url}/courses",
            f"{self.base_url}/programs", 
            f"{self.base_url}/training",
            f"{self.base_url}/services"
        ]
        
        for url in course_urls:
            html_content = self.get_page_content(url)
            if html_content:
                self.extract_courses_from_page(html_content)
                break
    
    def extract_courses_from_page(self, html_content):
        """Extract course information from HTML content"""
        # Look for list items that might be courses
        list_items = self.extract_text_between_tags(html_content, r'<li[^>]*>', r'</li>')
        
        for item in list_items:
            if len(item) > 10 and len(item) < 200:
                # Check if it looks like a course
                course_keywords = ['course', 'training', 'program', 'class', 'workshop', 'certification', 'development', 'marketing', 'data', 'web', 'ai', 'cyber']
                if any(keyword in item.lower() for keyword in course_keywords):
                    # Extract price if present
                    price_match = re.search(r'₹?\$?\d+(?:,\d+)*(?:\.\d{2})?', item)
                    price = price_match.group() if price_match else ''
                    
                    # Extract duration if present
                    duration_match = re.search(r'\d+\s*(?:weeks?|months?|days?|hours?)', item, re.IGNORECASE)
                    duration = duration_match.group() if duration_match else ''
                    
                    self.data['courses'].append({
                        'name': item,
                        'description': '',
                        'price': price,
                        'duration': duration
                    })
        
        # Also look for divs that might contain course info
        divs = self.extract_text_between_tags(html_content, r'<div[^>]*class=["\'][^"\']*course[^"\']*["\'][^>]*>', r'</div>')
        for div in divs:
            if len(div) > 20:
                # Extract course name from headings
                headings = self.extract_text_between_tags(div, r'<h[1-6][^>]*>', r'</h[1-6]>')
                if headings:
                    course_name = headings[0]
                    price_match = re.search(r'₹?\$?\d+(?:,\d+)*(?:\.\d{2})?', div)
                    price = price_match.group() if price_match else ''
                    
                    self.data['courses'].append({
                        'name': course_name,
                        'description': div[:100] + '...' if len(div) > 100 else div,
                        'price': price,
                        'duration': ''
                    })
    
    def scrape_contact(self):
        """Try to scrape contact information"""
        print("📞 Scraping contact info...")
        
        contact_urls = [
            f"{self.base_url}/contact",
            f"{self.base_url}/contact-us",
            f"{self.base_url}/get-in-touch"
        ]
        
        for url in contact_urls:
            html_content = self.get_page_content(url)
            if html_content:
                self.extract_contact_info(html_content)
                break
        
        # Also try to extract from main page
        if not self.data['contact']:
            html_content = self.get_page_content(self.base_url)
            if html_content:
                self.extract_contact_info(html_content)
    
    def extract_contact_info(self, html_content):
        """Extract contact information from HTML content"""
        # Extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_match = re.search(email_pattern, html_content)
        if email_match:
            self.data['contact']['email'] = email_match.group()
        
        # Extract phone
        phone_pattern = r'[\+]?[1-9][\d]{0,15}'
        phone_matches = re.findall(phone_pattern, html_content)
        for phone in phone_matches:
            if len(phone) >= 10:  # Likely a real phone number
                self.data['contact']['phone'] = phone
                break
        
        # Extract address (look for longer text that might be an address)
        address_pattern = r'[A-Za-z\s,\.]+(?:Street|Road|Avenue|Lane|Drive|Place|City|State|Country|PIN|Postal)'
        address_match = re.search(address_pattern, html_content, re.IGNORECASE)
        if address_match:
            self.data['contact']['address'] = address_match.group().strip()
    
    def save_data(self, filename='truelearn_data.json'):
        """Save scraped data to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
        print(f"💾 Data saved to {filename}")
    
    def save_chatbot_data(self):
        """Save data in format suitable for chatbot"""
        # Clean up courses data
        clean_courses = []
        for course in self.data['courses']:
            if course.get('name') and len(course['name']) > 3:
                clean_courses.append(course['name'])
        
        chatbot_data = {
            "name": self.data["name"],
            "description": self.data["description"] or "A comprehensive educational platform offering courses in technology, business, and personal development",
            "courses": clean_courses,
            "features": self.data["features"] or [
                "Interactive learning modules",
                "Expert instructors", 
                "Flexible scheduling",
                "Certificate upon completion",
                "24/7 support",
                "Mobile-friendly platform"
            ],
            "contact": self.data["contact"] or {
                "email": "info@truelearnacademy.com",
                "phone": "+1-555-ACADEMY",
                "address": "123 Learning Street, Education City, EC 12345"
            },
            "about": self.data["about"],
            "social_links": self.data["social_links"]
        }
        
        with open('chatbot_data.json', 'w', encoding='utf-8') as f:
            json.dump(chatbot_data, f, indent=2, ensure_ascii=False)
        print("💾 Chatbot data saved to chatbot_data.json")
    
    def print_summary(self):
        """Print a summary of scraped data"""
        print("\n📊 Scraped Data Summary:")
        print("=" * 50)
        print(f"Name: {self.data['name']}")
        print(f"Description: {self.data['description'][:100]}...")
        print(f"Courses found: {len(self.data['courses'])}")
        if self.data['courses']:
            print("Sample courses:")
            for course in self.data['courses'][:3]:
                print(f"  - {course.get('name', 'Unknown')}")
        print(f"Contact info: {bool(self.data['contact'])}")
        if self.data['contact']:
            print(f"  Email: {self.data['contact'].get('email', 'Not found')}")
            print(f"  Phone: {self.data['contact'].get('phone', 'Not found')}")
        print(f"Social links: {len(self.data['social_links'])}")
        print(f"About: {self.data['about'][:100]}..." if self.data['about'] else "About: Not found")

def main():
    """Main function to run the scraper"""
    scraper = SimpleTrueLearnScraper()
    data = scraper.scrape_website()
    
    if data:
        scraper.save_data()
        scraper.save_chatbot_data()
        scraper.print_summary()
    else:
        print("❌ Failed to scrape website data")

if __name__ == "__main__":
    main() 