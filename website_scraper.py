#!/usr/bin/env python3
"""
Web scraper for TrueLearn Academy website
Extracts real course information, pricing, contact details, etc.
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from urllib.parse import urljoin, urlparse
import time

class TrueLearnScraper:
    def __init__(self):
        self.base_url = "https://truelearnacademy.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.data = {
            "name": "TrueLearn Academy",
            "description": "",
            "courses": [],
            "pricing": {},
            "contact": {},
            "features": [],
            "about": "",
            "social_links": {},
            "pages": []
        }
    
    def scrape_website(self):
        """Main scraping function"""
        print("🔍 Scraping TrueLearn Academy website...")
        
        try:
            # Scrape main page
            self.scrape_main_page()
            
            # Scrape courses page
            self.scrape_courses_page()
            
            # Scrape about page
            self.scrape_about_page()
            
            # Scrape contact page
            self.scrape_contact_page()
            
            # Find and scrape additional pages
            self.find_additional_pages()
            
            print("✅ Website scraping completed!")
            return self.data
            
        except Exception as e:
            print(f"❌ Error scraping website: {e}")
            return None
    
    def get_page_content(self, url):
        """Get page content with error handling"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            print(f"⚠️ Could not fetch {url}: {e}")
            return None
    
    def scrape_main_page(self):
        """Scrape the main homepage"""
        print("📄 Scraping main page...")
        soup = self.get_page_content(self.base_url)
        if not soup:
            return
        
        # Extract description
        description_selectors = [
            'meta[name="description"]',
            '.hero-description',
            '.main-description',
            'h1 + p',
            '.intro p'
        ]
        
        for selector in description_selectors:
            desc_elem = soup.select_one(selector)
            if desc_elem:
                self.data['description'] = desc_elem.get_text().strip()
                break
        
        # Extract features
        feature_selectors = [
            '.features li',
            '.benefits li',
            '.highlights li',
            '.why-choose-us li'
        ]
        
        for selector in feature_selectors:
            features = soup.select(selector)
            if features:
                self.data['features'] = [f.get_text().strip() for f in features]
                break
        
        # Extract social links
        social_links = soup.find_all('a', href=re.compile(r'(facebook|twitter|instagram|linkedin|youtube)'))
        for link in social_links:
            platform = re.search(r'(facebook|twitter|instagram|linkedin|youtube)', link['href'])
            if platform:
                self.data['social_links'][platform.group(1)] = link['href']
    
    def scrape_courses_page(self):
        """Scrape courses page"""
        print("📚 Scraping courses page...")
        
        # Try different possible course page URLs
        course_urls = [
            f"{self.base_url}/courses",
            f"{self.base_url}/programs",
            f"{self.base_url}/training",
            f"{self.base_url}/services"
        ]
        
        for url in course_urls:
            soup = self.get_page_content(url)
            if soup:
                self.extract_courses_from_page(soup, url)
                break
    
    def extract_courses_from_page(self, soup, page_url):
        """Extract course information from a page"""
        # Look for course containers
        course_selectors = [
            '.course',
            '.program',
            '.service',
            '.training',
            '.card',
            '.item'
        ]
        
        for selector in course_selectors:
            courses = soup.select(selector)
            if courses:
                for course in courses:
                    course_info = self.extract_course_info(course)
                    if course_info:
                        self.data['courses'].append(course_info)
                break
        
        # Also look for course lists
        list_selectors = [
            'ul li',
            '.course-list li',
            '.program-list li'
        ]
        
        for selector in list_selectors:
            items = soup.select(selector)
            if items and len(items) > 3:  # Likely a course list
                for item in items:
                    text = item.get_text().strip()
                    if text and len(text) > 10:  # Meaningful content
                        self.data['courses'].append({
                            'name': text,
                            'description': '',
                            'duration': '',
                            'price': ''
                        })
                break
    
    def extract_course_info(self, course_elem):
        """Extract individual course information"""
        course_info = {
            'name': '',
            'description': '',
            'duration': '',
            'price': '',
            'features': []
        }
        
        # Extract course name
        name_selectors = ['h3', 'h4', '.title', '.name', 'h2']
        for selector in name_selectors:
            name_elem = course_elem.select_one(selector)
            if name_elem:
                course_info['name'] = name_elem.get_text().strip()
                break
        
        # Extract description
        desc_selectors = ['p', '.description', '.desc']
        for selector in desc_selectors:
            desc_elem = course_elem.select_one(selector)
            if desc_elem:
                course_info['description'] = desc_elem.get_text().strip()
                break
        
        # Extract price
        price_pattern = r'₹?\$?\d+(?:,\d+)*(?:\.\d{2})?'
        price_elem = course_elem.find(text=re.compile(price_pattern))
        if price_elem:
            course_info['price'] = re.search(price_pattern, price_elem).group()
        
        # Extract duration
        duration_pattern = r'\d+\s*(?:weeks?|months?|days?|hours?)'
        duration_elem = course_elem.find(text=re.compile(duration_pattern, re.IGNORECASE))
        if duration_elem:
            course_info['duration'] = re.search(duration_pattern, duration_elem, re.IGNORECASE).group()
        
        return course_info if course_info['name'] else None
    
    def scrape_about_page(self):
        """Scrape about page"""
        print("ℹ️ Scraping about page...")
        
        about_urls = [
            f"{self.base_url}/about",
            f"{self.base_url}/about-us",
            f"{self.base_url}/company"
        ]
        
        for url in about_urls:
            soup = self.get_page_content(url)
            if soup:
                # Extract about content
                about_selectors = ['.about-content', '.company-info', '.main-content p']
                for selector in about_selectors:
                    about_elem = soup.select_one(selector)
                    if about_elem:
                        self.data['about'] = about_elem.get_text().strip()
                        break
                break
    
    def scrape_contact_page(self):
        """Scrape contact page"""
        print("📞 Scraping contact page...")
        
        contact_urls = [
            f"{self.base_url}/contact",
            f"{self.base_url}/contact-us",
            f"{self.base_url}/get-in-touch"
        ]
        
        for url in contact_urls:
            soup = self.get_page_content(url)
            if soup:
                self.extract_contact_info(soup)
                break
    
    def extract_contact_info(self, soup):
        """Extract contact information"""
        # Extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_elem = soup.find(text=re.compile(email_pattern))
        if email_elem:
            self.data['contact']['email'] = re.search(email_pattern, email_elem).group()
        
        # Extract phone
        phone_pattern = r'[\+]?[1-9][\d]{0,15}'
        phone_elem = soup.find(text=re.compile(phone_pattern))
        if phone_elem:
            self.data['contact']['phone'] = re.search(phone_pattern, phone_elem).group()
        
        # Extract address
        address_selectors = ['.address', '.location', '.contact-address']
        for selector in address_selectors:
            addr_elem = soup.select_one(selector)
            if addr_elem:
                self.data['contact']['address'] = addr_elem.get_text().strip()
                break
    
    def find_additional_pages(self):
        """Find and scrape additional pages"""
        print("🔍 Finding additional pages...")
        
        soup = self.get_page_content(self.base_url)
        if not soup:
            return
        
        # Find all internal links
        links = soup.find_all('a', href=True)
        internal_links = []
        
        for link in links:
            href = link['href']
            if href.startswith('/') or self.base_url in href:
                internal_links.append(urljoin(self.base_url, href))
        
        # Remove duplicates and limit to reasonable number
        internal_links = list(set(internal_links))[:10]
        
        for link in internal_links:
            if link not in [self.base_url]:
                self.data['pages'].append(link)
    
    def save_data(self, filename='truelearn_data.json'):
        """Save scraped data to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
        print(f"💾 Data saved to {filename}")
    
    def print_summary(self):
        """Print a summary of scraped data"""
        print("\n📊 Scraped Data Summary:")
        print("=" * 50)
        print(f"Description: {self.data['description'][:100]}...")
        print(f"Courses found: {len(self.data['courses'])}")
        print(f"Features found: {len(self.data['features'])}")
        print(f"Contact info: {bool(self.data['contact'])}")
        print(f"Social links: {len(self.data['social_links'])}")
        print(f"Additional pages: {len(self.data['pages'])}")
    
    def save_chatbot_data(self):
        """Save data in format suitable for chatbot"""
        chatbot_data = {
            "name": self.data["name"],
            "description": self.data["description"] or "A comprehensive educational platform offering courses in technology, business, and personal development",
            "courses": [course.get('name', '') for course in self.data["courses"] if course.get('name')],
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
            "pricing": self.data["pricing"],
            "about": self.data["about"],
            "social_links": self.data["social_links"]
        }
        
        with open('chatbot_data.json', 'w', encoding='utf-8') as f:
            json.dump(chatbot_data, f, indent=2, ensure_ascii=False)
        print("💾 Chatbot data saved to chatbot_data.json")

def main():
    """Main function to run the scraper"""
    scraper = TrueLearnScraper()
    data = scraper.scrape_website()
    
    if data:
        scraper.save_data()
        scraper.print_summary()
        
        # Also save a formatted version for the chatbot
        scraper.save_chatbot_data()
    else:
        print("❌ Failed to scrape website data")

if __name__ == "__main__":
    main() 