#!/usr/bin/env python3
"""
Test script for the articles capture workflow
"""

import sys
import os
import tempfile
import json
import time
from datetime import datetime
import re
from bs4 import BeautifulSoup

# Mock config for testing
class MockConfig:
    ARTICLES_DIR = "articles"

# Create a standalone ArticleProcessor for testing without config dependency
class TestArticleProcessor:
    """Test version of ArticleProcessor without config dependency"""
    
    def __init__(self, articles_dir="articles"):
        self.articles_dir = articles_dir
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
                from dateutil.parser import parse as parse_date
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
                return False
            
            # Format date for display
            if isinstance(published, (int, float)):
                date_obj = datetime.fromtimestamp(published)
            else:
                from dateutil.parser import parse as parse_date
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
            
            return True
            
        except Exception as e:
            return False

def test_article_processor():
    """Test the ArticleProcessor functionality"""
    print("Testing ArticleProcessor...")
    
    # Create a temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        processor = TestArticleProcessor(temp_dir)
        
        # Test article data
        test_article = {
            'title': 'Test Medical Research Article',
            'published': 1640995200,  # 2022-01-01
            'author': 'Dr. John Smith',
            'origin': {
                'title': 'Medical Journal RSS',
                'htmlUrl': 'https://example.com/feed'
            },
            'summary': {
                'content': '<p>This is a <strong>test article</strong> with <em>HTML content</em>. <a href="https://example.com">Link here</a>.</p>'
            },
            'alternate': [
                {'type': 'text/html', 'href': 'https://example.com/article/123'}
            ]
        }
        
        # Test saving article
        success = processor.save_article(test_article)
        if success:
            print("✓ Article saved successfully")
        else:
            print("✗ Failed to save article")
            return False
        
        # Check if file was created
        files = os.listdir(temp_dir)
        if files:
            print(f"✓ File created: {files[0]}")
            
            # Read and check content
            with open(os.path.join(temp_dir, files[0]), 'r') as f:
                content = f.read()
            
            # Basic checks
            if 'Test Medical Research Article' in content:
                print("✓ Title preserved")
            else:
                print("✗ Title missing")
                return False
                
            if '**test article**' in content:
                print("✓ HTML bold converted to markdown")
            else:
                print("✗ HTML conversion failed")
                return False
                
            if '[Link here](https://example.com)' in content:
                print("✓ HTML link converted to markdown")
            else:
                print("✗ Link conversion failed")
                return False
                
        else:
            print("✗ No file created")
            return False
    
    return True

def test_html_cleaning():
    """Test HTML content cleaning"""
    print("\nTesting HTML cleaning...")
    
    processor = TestArticleProcessor("/tmp")  # Directory doesn't matter for this test
    
    test_html = """
    <div>
        <h1>Title</h1>
        <p>This is a <strong>bold</strong> and <em>italic</em> text.</p>
        <p>Link: <a href="https://example.com">Example</a></p>
        <script>alert('malicious');</script>
        <style>body{color:red;}</style>
    </div>
    """
    
    cleaned = processor.clean_html_content(test_html)
    
    if 'alert(' not in cleaned:
        print("✓ Script tags removed")
    else:
        print("✗ Script tags not removed")
        return False
        
    if 'color:red' not in cleaned:
        print("✓ Style tags removed")
    else:
        print("✗ Style tags not removed")
        return False
        
    if '**bold**' in cleaned:
        print("✓ Bold tags converted")
    else:
        print("✗ Bold tags not converted")
        return False
        
    if '*italic*' in cleaned:
        print("✓ Italic tags converted")
    else:
        print("✗ Italic tags not converted")
        return False
    
    if '[Example](https://example.com)' in cleaned:
        print("✓ Links converted")
    else:
        print("✗ Links not converted")
        return False
    
    return True

def test_filename_generation():
    """Test filename generation"""
    print("\nTesting filename generation...")
    
    processor = TestArticleProcessor("/tmp")
    
    # Test with normal title
    filename = processor.generate_filename("Medical Research: New Breakthrough!", 1640995200)
    if filename.startswith("2022-01-01_") and filename.endswith(".md"):
        print("✓ Filename format correct")
    else:
        print(f"✗ Filename format incorrect: {filename}")
        return False
    
    # Test with problematic characters
    filename = processor.generate_filename("Title with/special\\chars:and|pipes", 1640995200)
    if "/" not in filename and "\\" not in filename and ":" not in filename:
        print("✓ Special characters cleaned")
    else:
        print(f"✗ Special characters not cleaned: {filename}")
        return False
    
    return True

def main():
    """Run all tests"""
    print("Running Articles Capture Tests")
    print("=" * 40)
    
    tests = [
        test_html_cleaning,
        test_filename_generation,
        test_article_processor,
    ]
    
    passed = 0
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                print(f"Test {test.__name__} FAILED")
        except Exception as e:
            print(f"Test {test.__name__} ERROR: {e}")
    
    print("\n" + "=" * 40)
    print(f"Tests passed: {passed}/{len(tests)}")
    
    if passed == len(tests):
        print("All tests passed! ✓")
        return True
    else:
        print("Some tests failed! ✗")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)