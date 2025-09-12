#!/usr/bin/env python3
"""
Inoreader Articles Capture Workflow
Fetches articles from Inoreader and saves them as markdown files.
"""

import os
import sys
import json
import requests
import re
from datetime import datetime, timedelta
from dateutil.parser import parse as parse_date
from bs4 import BeautifulSoup
import time

# Try to import config, fallback to template if not available
try:
    import config
except ImportError:
    print("Config file not found. Please copy config_template.py to config.py and configure your credentials.")
    sys.exit(1)


class InoreaderClient:
    """Client for Inoreader API"""
    
    def __init__(self):
        self.app_id = config.INOREADER_APP_ID
        self.app_key = config.INOREADER_APP_KEY
        self.username = config.INOREADER_USERNAME
        self.password = config.INOREADER_PASSWORD
        self.base_url = config.INOREADER_API_BASE
        self.auth_url = config.INOREADER_AUTH_URL
        self.access_token = None
        self.session = requests.Session()
        
    def authenticate(self):
        """Authenticate with Inoreader API using OAuth2"""
        auth_data = {
            'client_id': self.app_id,
            'client_secret': self.app_key,
            'grant_type': 'password',
            'username': self.username,
            'password': self.password,
            'scope': 'read'
        }
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        try:
            response = self.session.post(self.auth_url, data=auth_data, headers=headers)
            response.raise_for_status()
            
            auth_response = response.json()
            self.access_token = auth_response.get('access_token')
            
            if not self.access_token:
                raise Exception("No access token received")
                
            # Set authorization header for future requests
            self.session.headers.update({
                'Authorization': f'Bearer {self.access_token}'
            })
            
            print("Successfully authenticated with Inoreader API")
            return True
            
        except Exception as e:
            print(f"Authentication failed: {e}")
            return False
    
    def get_subscription_list(self):
        """Get list of subscribed feeds"""
        url = f"{self.base_url}subscription/list"
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching subscriptions: {e}")
            return None
    
    def get_unread_items(self, max_items=None):
        """Get unread items from all subscriptions"""
        if max_items is None:
            max_items = config.MAX_ARTICLES
            
        url = f"{self.base_url}stream/contents/user/-/state/com.google/reading-list"
        
        params = {
            'xt': 'user/-/state/com.google/read',  # exclude read items
            'n': max_items,
            'output': 'json'
        }
        
        # Only get items from the last N days
        since_timestamp = int((datetime.now() - timedelta(days=config.DAYS_BACK)).timestamp())
        params['ot'] = since_timestamp
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching unread items: {e}")
            return None


class ArticleProcessor:
    """Processes and saves articles as markdown files"""
    
    def __init__(self, articles_dir=None):
        self.articles_dir = articles_dir or config.ARTICLES_DIR
        self.ensure_articles_dir()
    
    def ensure_articles_dir(self):
        """Ensure articles directory exists"""
        if not os.path.exists(self.articles_dir):
            os.makedirs(self.articles_dir)
    
    def clean_html_content(self, html_content):
        """Clean HTML content and convert to markdown-friendly text"""
        if not html_content:
            return ""
            
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Convert common HTML elements to markdown
        for tag in soup.find_all(['strong', 'b']):
            tag.replace_with(f"**{tag.get_text()}**")
            
        for tag in soup.find_all(['em', 'i']):
            tag.replace_with(f"*{tag.get_text()}*")
            
        for tag in soup.find_all('a'):
            href = tag.get('href', '')
            text = tag.get_text()
            tag.replace_with(f"[{text}]({href})")
        
        # Get text and clean up
        text = soup.get_text()
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        text = '\n'.join(line for line in lines if line)
        
        return text
    
    def generate_filename(self, title, published_date):
        """Generate a safe filename from title and date"""
        # Parse date
        try:
            if isinstance(published_date, (int, float)):
                date_obj = datetime.fromtimestamp(published_date)
            else:
                date_obj = parse_date(published_date)
        except:
            date_obj = datetime.now()
        
        date_str = date_obj.strftime("%Y-%m-%d")
        
        # Clean title for filename
        safe_title = re.sub(r'[^\w\s-]', '', title.strip())
        safe_title = re.sub(r'[-\s]+', '-', safe_title)
        safe_title = safe_title[:50]  # Limit length
        
        return f"{date_str}_{safe_title}.md"
    
    def save_article(self, article_data):
        """Save article as markdown file"""
        try:
            title = article_data.get('title', 'Untitled')
            published = article_data.get('published', time.time())
            author = article_data.get('author', 'Unknown')
            origin_title = article_data.get('origin', {}).get('title', '')
            origin_url = article_data.get('origin', {}).get('htmlUrl', '')
            content = article_data.get('summary', {}).get('content', '') or article_data.get('content', {}).get('content', '')
            canonical_url = next((link['href'] for link in article_data.get('alternate', []) if link.get('type') == 'text/html'), '')
            
            # Clean content
            clean_content = self.clean_html_content(content)
            
            # Generate filename
            filename = self.generate_filename(title, published)
            filepath = os.path.join(self.articles_dir, filename)
            
            # Skip if file already exists
            if os.path.exists(filepath):
                print(f"Article already exists: {filename}")
                return False
            
            # Format date for display
            if isinstance(published, (int, float)):
                date_obj = datetime.fromtimestamp(published)
            else:
                date_obj = parse_date(str(published))
            formatted_date = date_obj.strftime("%Y-%m-%d %H:%M:%S")
            
            # Create markdown content
            markdown_content = f"""# {title}

**Source:** {origin_title}  
**Author:** {author}  
**Published:** {formatted_date}  
**URL:** {canonical_url}  
**Feed:** {origin_url}  

---

{clean_content}

---
*Captured from Inoreader on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""
            
            # Save file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            print(f"Saved article: {filename}")
            return True
            
        except Exception as e:
            print(f"Error saving article '{article_data.get('title', 'Unknown')}': {e}")
            return False


def main():
    """Main workflow function"""
    print("Starting Inoreader Articles Capture Workflow")
    print("-" * 50)
    
    # Initialize client
    client = InoreaderClient()
    
    # Authenticate
    if not client.authenticate():
        print("Failed to authenticate. Please check your credentials in config.py")
        return False
    
    # Get subscriptions (for info)
    subs = client.get_subscription_list()
    if subs and 'subscriptions' in subs:
        print(f"Found {len(subs['subscriptions'])} subscribed feeds")
    
    # Get unread articles
    print("Fetching unread articles...")
    items_data = client.get_unread_items()
    
    if not items_data or 'items' not in items_data:
        print("No articles found or error fetching articles")
        return False
    
    articles = items_data['items']
    print(f"Found {len(articles)} unread articles")
    
    if not articles:
        print("No new articles to process")
        return True
    
    # Process articles
    processor = ArticleProcessor()
    saved_count = 0
    
    for article in articles:
        if processor.save_article(article):
            saved_count += 1
    
    print("-" * 50)
    print(f"Workflow completed: {saved_count} articles saved")
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)