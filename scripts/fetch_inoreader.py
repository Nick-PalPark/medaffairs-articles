#!/usr/bin/env python3
"""
Fetch articles from Inoreader and generate articles.json for medaffairs.tech

This script:
1. Fetches tagged items from Inoreader API
2. Optionally generates snappy headlines using OpenAI
3. Normalizes article data
4. Preserves manual_title overrides
5. Enforces heroes/columns limits
6. Updates articles.json
"""

import os
import json
import requests
import time
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
import hashlib
import re

# Configuration
INOREADER_API_BASE = "https://www.inoreader.com/reader/api/0"
MAX_HEROES = int(os.environ.get("MAX_HEROES", "3"))
MAX_COLUMNS = int(os.environ.get("MAX_COLUMNS", "6"))
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
INOREADER_APP_ID = os.environ.get("INOREADER_APP_ID")
INOREADER_API_KEY = os.environ.get("INOREADER_API_KEY")
TARGET_TAG = os.environ.get("INOREADER_TAG", "medaffairs")


class InoreaderFetcher:
    """Handles Inoreader API interactions"""
    
    def __init__(self, app_id: str, api_key: str):
        self.app_id = app_id
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'MedAffairs/1.0',
            'Authorization': f'Bearer {api_key}'
        })
    
    def get_tagged_items(self, tag: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Fetch items with specific tag from Inoreader"""
        try:
            # Use stream contents endpoint to get tagged items
            url = f"{INOREADER_API_BASE}/stream/contents"
            params = {
                's': f'user/-/label/{tag}',  # Stream ID for tagged items
                'n': limit,  # Number of items
                'ot': int(time.time() - 7*24*60*60),  # Items from last 7 days
                'output': 'json'
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            return data.get('items', [])
            
        except requests.RequestException as e:
            print(f"Error fetching from Inoreader: {e}")
            return []


class OpenAIGenerator:
    """Handles OpenAI API interactions for headline generation"""
    
    def __init__(self, api_key: Optional[str]):
        self.api_key = api_key
        self.enabled = bool(api_key)
    
    def generate_headline(self, title: str, content: str) -> Optional[str]:
        """Generate a snappy headline using OpenAI"""
        if not self.enabled:
            return None
        
        try:
            import openai
            openai.api_key = self.api_key
            
            prompt = f"""
            Create a snappy, engaging headline for this medical affairs article.
            Keep it under 80 characters, professional but attention-grabbing.
            
            Original title: {title}
            Content preview: {content[:500]}...
            
            Return only the headline, no quotes or extra text.
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=50,
                temperature=0.7
            )
            
            headline = response.choices[0].message.content.strip()
            return headline if len(headline) <= 80 else title
            
        except Exception as e:
            print(f"Error generating headline with OpenAI: {e}")
            return None


class ArticleNormalizer:
    """Normalizes and processes article data"""
    
    @staticmethod
    def generate_article_id(title: str, url: str) -> str:
        """Generate consistent article ID from title and URL"""
        combined = f"{title}{url}"
        return hashlib.md5(combined.encode()).hexdigest()[:12]
    
    @staticmethod
    def clean_html(html_content: str) -> str:
        """Basic HTML cleaning and text extraction"""
        # Remove HTML tags (basic implementation)
        clean = re.sub(r'<[^>]+>', '', html_content)
        # Clean up whitespace
        clean = re.sub(r'\s+', ' ', clean).strip()
        return clean
    
    @staticmethod
    def extract_summary(content: str, max_length: int = 200) -> str:
        """Extract summary from content"""
        if len(content) <= max_length:
            return content
        
        # Find the last sentence that fits within the limit
        sentences = content.split('. ')
        summary = ""
        for sentence in sentences:
            if len(summary + sentence + '. ') <= max_length:
                summary += sentence + '. '
            else:
                break
        
        return summary.strip() if summary else content[:max_length] + '...'
    
    def normalize_article(self, item: Dict[str, Any], ai_headline: Optional[str] = None) -> Dict[str, Any]:
        """Convert Inoreader item to normalized article format"""
        # Extract basic info
        title = item.get('title', 'Untitled')
        url = item.get('canonical', [{}])[0].get('href') if item.get('canonical') else None
        
        if not url:
            # Try alternate URL sources
            url = item.get('alternate', [{}])[0].get('href', '')
        
        # Generate article ID
        article_id = self.generate_article_id(title, url)
        
        # Extract and clean content
        content_obj = item.get('summary', {})
        html_content = content_obj.get('content', '') if isinstance(content_obj, dict) else str(content_obj)
        clean_content = self.clean_html(html_content)
        
        # Extract metadata
        published_timestamp = item.get('published', time.time())
        published_date = datetime.fromtimestamp(published_timestamp, timezone.utc).isoformat()
        
        # Extract tags/categories
        tags = []
        for category in item.get('categories', []):
            if isinstance(category, str):
                # Extract tag from category string like "user/1234/label/tag"
                if '/label/' in category:
                    tag = category.split('/label/')[-1]
                    tags.append(tag)
        
        # Build normalized article
        article = {
            'id': article_id,
            'title': title,
            'manual_title': None,  # For manual overrides
            'generated_headline': ai_headline,
            'url': url,
            'content': clean_content,
            'summary': self.extract_summary(clean_content),
            'published_date': published_date,
            'fetched_date': datetime.now(timezone.utc).isoformat(),
            'tags': tags,
            'source': item.get('origin', {}).get('title', 'Unknown'),
            'author': item.get('author', 'Unknown'),
            'is_hero': False,
            'is_column': False
        }
        
        return article


def load_existing_articles(filepath: str) -> Dict[str, Any]:
    """Load existing articles.json file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            'articles': [],
            'heroes': [],
            'columns': [],
            'last_updated': None,
            'limits': {
                'max_heroes': MAX_HEROES,
                'max_columns': MAX_COLUMNS
            }
        }


def preserve_manual_titles(new_articles: List[Dict], existing_data: Dict) -> List[Dict]:
    """Preserve manual_title values from existing articles"""
    existing_articles = {article['id']: article for article in existing_data.get('articles', [])}
    
    for article in new_articles:
        article_id = article['id']
        if article_id in existing_articles:
            # Preserve manual overrides
            existing_article = existing_articles[article_id]
            article['manual_title'] = existing_article.get('manual_title')
            article['is_hero'] = existing_article.get('is_hero', False)
            article['is_column'] = existing_article.get('is_column', False)
    
    return new_articles


def enforce_limits(articles: List[Dict], max_heroes: int, max_columns: int) -> Dict[str, Any]:
    """Enforce hero and column limits"""
    # Separate articles by type
    heroes = [a for a in articles if a.get('is_hero', False)]
    columns = [a for a in articles if a.get('is_column', False)]
    regular_articles = [a for a in articles if not a.get('is_hero', False) and not a.get('is_column', False)]
    
    # Sort by published date (most recent first)
    heroes.sort(key=lambda x: x['published_date'], reverse=True)
    columns.sort(key=lambda x: x['published_date'], reverse=True)
    
    # Enforce limits
    if len(heroes) > max_heroes:
        # Move excess heroes to regular articles
        excess_heroes = heroes[max_heroes:]
        heroes = heroes[:max_heroes]
        for hero in excess_heroes:
            hero['is_hero'] = False
        regular_articles.extend(excess_heroes)
    
    if len(columns) > max_columns:
        # Move excess columns to regular articles  
        excess_columns = columns[max_columns:]
        columns = columns[:max_columns]
        for column in excess_columns:
            column['is_column'] = False
        regular_articles.extend(excess_columns)
    
    # Combine all articles
    all_articles = heroes + columns + regular_articles
    
    return {
        'articles': all_articles,
        'heroes': [a['id'] for a in heroes],
        'columns': [a['id'] for a in columns]
    }


def main():
    """Main execution function"""
    # Check required environment variables
    if not INOREADER_APP_ID or not INOREADER_API_KEY:
        print("Error: INOREADER_APP_ID and INOREADER_API_KEY are required")
        return 1
    
    # Initialize components
    fetcher = InoreaderFetcher(INOREADER_APP_ID, INOREADER_API_KEY)
    ai_generator = OpenAIGenerator(OPENAI_API_KEY)
    normalizer = ArticleNormalizer()
    
    # Load existing data
    articles_file = os.path.join(os.path.dirname(__file__), '..', 'articles.json')
    existing_data = load_existing_articles(articles_file)
    
    print(f"Fetching articles tagged with '{TARGET_TAG}' from Inoreader...")
    
    # Fetch new articles
    raw_items = fetcher.get_tagged_items(TARGET_TAG)
    print(f"Found {len(raw_items)} items")
    
    if not raw_items:
        print("No new articles found")
        return 0
    
    # Process articles
    new_articles = []
    for item in raw_items:
        try:
            # Generate AI headline if available
            ai_headline = None
            if ai_generator.enabled:
                ai_headline = ai_generator.generate_headline(
                    item.get('title', ''),
                    item.get('summary', {}).get('content', '') if isinstance(item.get('summary'), dict) else str(item.get('summary', ''))
                )
            
            # Normalize article
            article = normalizer.normalize_article(item, ai_headline)
            new_articles.append(article)
            
        except Exception as e:
            print(f"Error processing article: {e}")
            continue
    
    print(f"Successfully processed {len(new_articles)} articles")
    
    # Preserve manual titles and settings
    new_articles = preserve_manual_titles(new_articles, existing_data)
    
    # Enforce limits
    result = enforce_limits(new_articles, MAX_HEROES, MAX_COLUMNS)
    
    # Update metadata
    final_data = {
        'articles': result['articles'],
        'heroes': result['heroes'],
        'columns': result['columns'],
        'last_updated': datetime.now(timezone.utc).isoformat(),
        'limits': {
            'max_heroes': MAX_HEROES,
            'max_columns': MAX_COLUMNS
        }
    }
    
    # Save to file
    with open(articles_file, 'w', encoding='utf-8') as f:
        json.dump(final_data, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully updated articles.json with {len(final_data['articles'])} articles")
    print(f"Heroes: {len(final_data['heroes'])}/{MAX_HEROES}")
    print(f"Columns: {len(final_data['columns'])}/{MAX_COLUMNS}")
    
    return 0


if __name__ == '__main__':
    exit(main())